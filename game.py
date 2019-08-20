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

def main(): # 4 - 6 players
    # DEFINE VARIABLES
    msg_join = 'Congratulations!! You are joining the Werewolf Game'
    str_curr = 'Current players: \n'
    player = []

    ###############################################

    if incoming_msg == '/join': # If user type '/join'
        if isinstance(event.source, SourceGroup): # If eventnya dari group
            userid = []
            profile = line_bot_api.get_profile(event.source.user_id)
            if len(userid) >= 4 and len(userid) <= 6: # If total players antara 4-6
                for x in range(len(userid)): 
                    if profile.user_id != userid[x]: # If ada player baru
                        userid.append(profile.user_id) 
                        print('User ID: ' + userid)
                        line_bot_api.push_message(userid, TextSendMessage(msg_join))
                        for y in range(len(userid)):
                            player.append(str(y+1) + '. ' + profile.display_name)

                        players = '\n'.join(player)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(str_curr + players))
                            
                print('PLAYERS: ' + str(userid))

                
                if incoming_msg == '/startgame':
                    print('start game di click')
            elif len(userid) >= 7 and len(userid) <= 12:
                print('antara 7-12 players')



            elif len(userid) < 4:   # If players kurang dari 4
                line_bot_api.reply_message(event.reply_token, TextSendMessage('Sorry, you are too lonely (min 4 ppl)')

            elif len(userid) > 12:  # If players lebih dari 12
                line_bot_api.reply_message(event.reply_token, TextSendMessage('Sorry, you guys are too crowded (max 12 ppl)')
            
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage('Werewolf is under maintenance :)')



    if incoming_msg == '/quit':

                