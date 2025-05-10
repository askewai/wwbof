import os
from decouple import config
from flask import (Flask, request, abort)
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import InvalidSignatureError
import json
from linebot.models import (
    MessageEvent, 
    TextMessage, 
    TextSendMessage,
    SourceUser,
    SourceGroup,
    SourceRoom,
    MessageAction,
    LeaveEvent,
    JoinEvent
)
import requests
import time
import re
import random

# DEFINE GLOBAL VARIABLES
msg_join = 'Congratulations!! You are joining the Werewolf Game'
str_curr = 'Current players: \n'
players_arr = []
displayname = []
userid = []
state = 0

'''
0. Join state
1. startgame state
2. endgame
'''

def main(event, line_bot_api, handler, incoming_msg): 
    global state
    if state == 0:
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

    #########################################################
    ######################################################### STATE 1 (Start Game)
    #########################################################

    if incoming_msg == '/startgame' and state == 0:
        if isinstance(event.source, SourceGroup):
            if len(userid) >= 4 and len(userid) <= 6:
                state = 1
                groupid = event.source.group_id
                line_bot_api.reply_message(event.reply_token, TextSendMessage('The game has started!! \nAuuuuuuuwwww!! Who is the werewolf here? Let\'s find out!'))

                # Randomize roles for 4-6 players
                role = ['Werewolf', 'Seer']
                for y in range(len(userid)-2):
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
                    elif data[x]['role'] == 'Villager':
                        role_desc = 'You are just deadweight'
                    line_bot_api.push_message(data[x]['userid'], TextSendMessage(f'Your role is: {data[x]["role"]}\n{role_desc}'))

                # Start the Day and Night cycle
                night_phase(groupid, data)

            elif len(userid) < 4:
                line_bot_api.reply_message(event.reply_token, TextSendMessage('Sorry, you need at least 4 players to start the game.'))
            elif len(userid) > 6:
                line_bot_api.reply_message(event.reply_token, TextSendMessage('Sorry, the game supports up to 6 players.'))

    print('STATE: ' + str(state))

def night_phase(groupid, data):
    # Night phase: Werewolf picks a target to kill
    time.sleep(5)
    line_bot_api.push_message(groupid, TextSendMessage('🌙 It is now midnight. Some villagers have fallen asleep...'))
    
    # Example for Werewolf to pick a target
    target = 'Player2'  # Example, in reality this would be dynamic
    line_bot_api.push_message(groupid, TextSendMessage(f'Werewolf has chosen {target} as the target to kill.'))

    # Day phase: Announce the death
    time.sleep(5)
    line_bot_api.push_message(groupid, TextSendMessage(f'🌤 The Sun has risen, an unfortunate soul has departed. {target} was killed.'))

    # Continue with further game phases...
    # Implement voting, etc.

