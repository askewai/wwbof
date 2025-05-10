import random
import time
from linebot.models import TextSendMessage, SourceGroup  # Import these to fix the errors

# Global variables for tracking players and state
msg_join = 'Congratulations!! You are joining the Werewolf Game'
str_curr = 'Current players: \n'
players_arr = []
displayname = []
userid = []
state = 0  # Game state (0 = joined, 1 = started, 2 = ended)

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

                if len(userid) == 0:  # If players list is empty
                    userid.append(profile.user_id) 
                    displayname.append(profile.display_name)
                    players_arr.append(f'{len(userid)}. {profile.display_name}')
                    players = '\n'.join(players_arr)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(str_curr + players))

                elif len(userid) > 0:  # If players exist
                    if profile.user_id not in userid:  # If this is a new player
                        userid.append(profile.user_id) 
                        displayname.append(profile.display_name)
                        players_arr.append(f'{len(userid)}. {profile.display_name}')
                        players = '\n'.join(players_arr)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(str_curr + players))
                    else:  # If player is already in the game
                        line_bot_api.reply_message(event.reply_token, TextSendMessage('Sorry, you are already in the game'))

    # Start the game when /startgame is called and at least 4 players are joined
    if incoming_msg == '/startgame' and state == 0:
        if len(userid) >= 4:
            state = 1
            groupid = event.source.group_id
            line_bot_api.reply_message(event.reply_token, TextSendMessage('The game has started!! \nAuuuuuuuwwww!! Who is the werewolf here? Let\'s find out!'))

            # Randomize roles for 4-6 players
            role = ['Werewolf', 'Seer', 'Traitor', 'Orphan'] if len(userid) <= 6 else ['Werewolf', 'Seer', 'Werewolf']
            for _ in range(len(userid) - len(role)):
                role.append('Villager')

            random.shuffle(role)

            # Assign roles to players
            data = []
            for x in range(len(userid)):
                each_data = {
                    "userid": userid[x],
                    "displayname": displayname[x],
                    "role": role[x],
                    "status": True
                }
                data.append(each_data)

                # Send the role description to each player
                if data[x]['role'] == 'Werewolf':
                    role_desc = 'You can go WOLF TRIGGER and attack a player at night'
                elif data[x]['role'] == 'Seer':
                    role_desc = 'You can go STALKING at night to see a player\'s role'
                elif data[x]['role'] == 'Traitor':
                    role_desc = 'You can become a werewolf if the werewolf dies'
                elif data[x]['role'] == 'Orphan':
                    role_desc = 'You can make a player sleep with you'
                elif data[x]['role'] == 'Villager':
                    role_desc = 'You are just deadweight'
                
                line_bot_api.push_message(data[x]['userid'], TextSendMessage(f'Your role is: {data[x]["role"]}\n{role_desc}'))

            # Start the Day and Night cycle
            night_phase(groupid, data)

        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("Not enough players to start the game. Minimum 4 players required."))

def night_phase(groupid, data):
    # Handle the night phase: where players can interact based on their roles
    line_bot_api.push_message(groupid, TextSendMessage('It is now night. Players can take their actions.'))
    time.sleep(5)
    for player in data:
        if player['role'] == 'Seer':
            line_bot_api.push_message(player['userid'], TextSendMessage('Please select a player to check their role.'))
        elif player['role'] == 'Werewolf':
            line_bot_api.push_message(player['userid'], TextSendMessage('Please select a player to kill.'))
        elif player['role'] == 'Doctor':
            line_bot_api.push_message(player['userid'], TextSendMessage('Please select a player to protect.'))
        elif player['role'] == 'Orphan':
            line_bot_api.push_message(player['userid'], TextSendMessage('Please select a player to sleep with you.'))

    # Implement logic for each action after night phase and voting on the day phase
