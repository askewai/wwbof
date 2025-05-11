import random
import time
import mysql.connector
from mysql.connector import Error
from linebot.models import TextSendMessage, SourceGroup

# Global variables for tracking players and state
msg_join = 'Congratulations!! You are joining the Werewolf Game'
str_curr = 'Current players: \n'
players_arr = []
displayname = []
userid = []
state = 0  # Game state (0 = joined, 1 = started, 2 = ended)

# Database connection setup
def create_connection():
    """ Create a connection to the MySQL database """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='werewolf_game',
            user='root',  # replace with your MySQL username
            password='password'  # replace with your MySQL password
        )
        if connection.is_connected():
            print("Connection to MySQL database is successful")
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def quit_game(event, line_bot_api, handler):
    global state
    if state != 0:  # If the game has started or is in progress, we stop it
        state = 0
        line_bot_api.push_message(event.source.group_id, TextSendMessage(text="The game has been quit and will be reset."))
    else:
        line_bot_api.push_message(event.source.group_id, TextSendMessage(text="No game is currently running."))

def main(event, line_bot_api, handler, incoming_msg): 
    global state
    if state == 0:  # Waiting for players to join
        if incoming_msg == '/join':  # If user types '/join'
            if isinstance(event.source, SourceGroup):  # If event is from a group
                profile = line_bot_api.get_profile(event.source.user_id)

                # Insert player into the database
                connection = create_connection()
                if connection:
                    cursor = connection.cursor()
                    cursor.execute('''
                        INSERT INTO players (userid, displayname, role, status)
                        VALUES (%s, %s, %s, %s)
                    ''', (profile.user_id, profile.display_name, 'Villager', True))
                    connection.commit()
                    cursor.close()
                    connection.close()

                # Send confirmation message
                line_bot_api.reply_message(event.reply_token, TextSendMessage(f"{profile.display_name} has joined the game"))

    # Start the game when /startgame is called and at least 4 players are joined
    if incoming_msg == '/startgame' and state == 0:
        # Retrieve all players from the database
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM players WHERE status = TRUE')
            players = cursor.fetchall()
            connection.close()

        if len(players) >= 4:
            state = 1
            groupid = event.source.group_id
            line_bot_api.reply_message(event.reply_token, TextSendMessage('The game has started!! \nAuuuuuuuwwww!! Who is the werewolf here? Let\'s find out!'))

            # Randomize roles for 4-6 players
            role = ['Werewolf', 'Seer', 'Traitor', 'Orphan'] if len(players) <= 6 else ['Werewolf', 'Seer', 'Werewolf']
            for _ in range(len(players) - len(role)):
                role.append('Villager')

            random.shuffle(role)

            # Assign roles to players and update in the database
            for x in range(len(players)):
                user_id = players[x][1]  # Get user_id from the database row
                player_role = role[x]
                
                # Update player's role in the database
                connection = create_connection()
                if connection:
                    cursor = connection.cursor()
                    cursor.execute('''
                        UPDATE players
                        SET role = %s
                        WHERE userid = %s
                    ''', (player_role, user_id))
                    connection.commit()
                    cursor.close()
                    connection.close()

                # Send the role description to each player
                role_desc = 'You are just deadweight'
                if player_role == 'Werewolf':
                    role_desc = 'You can go WOLF TRIGGER and attack a player at night'
                elif player_role == 'Seer':
                    role_desc = 'You can go STALKING at night to see a player\'s role'
                elif player_role == 'Traitor':
                    role_desc = 'You can become a werewolf if the werewolf dies'
                elif player_role == 'Orphan':
                    role_desc = 'You can make a player sleep with you'
                
                line_bot_api.push_message(user_id, TextSendMessage(f'Your role is: {player_role}\n{role_desc}'))

            # Start the Day and Night cycle
            night_phase(groupid)

        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("Not enough players to start the game. Minimum 4 players required."))

def night_phase(groupid):
    # Handle the night phase: where players can interact based on their roles
    line_bot_api.push_message(groupid, TextSendMessage('It is now night. Players can take their actions.'))
    time.sleep(5)
    # Logic for interactions (Seer, Werewolf, Doctor, Orphan, etc.) goes here

