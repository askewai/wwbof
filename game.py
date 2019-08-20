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

def main(): # 4 - 6 players
    # DEFINE VARIABLES
    msg_join = 'Congratulations!! You are joining the Werewolf Game'


    ###############################################

    if incoming_msg == '/join':
        if isinstance(event.source, SourceGroup):
            userid = []
            profile = line_bot_api.get_profile(event.source.user_id)
            for x in range(len(userid)): # 0 - 2
                if profile.user_id != userid[x]:
                    userid.append(profile.user_id) 
                    print('User ID: ' + userid)
                    print('Start sending to ' + profile.display_name)
                    line_bot_api.push_message(userid, TextSendMessage(msg_join))
            
            print('Users that join the game ' + str(userid))
            
            if incoming_msg == '/startgame':
                