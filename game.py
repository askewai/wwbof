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
1. startgame stat
2. endgame
'''

##################################################################################

def main(event, line_bot_api, handler, incoming_msg): 
    global state
    if state == 0:
        if incoming_msg == '/join': # If user type '/join'
            if isinstance(event.source, SourceGroup): # If eventnya dari group
                profile = line_bot_api.get_profile(event.source.user_id)

                if len(userid) == 0: # If players is still null
                    userid.append(profile.user_id) 
                    displayname.append(profile.display_name)
                    print('Add user ID: ' + profile.user_id)
                    line_bot_api.push_message(profile.user_id, TextSendMessage(msg_join))
                    
                    # Announce who are the players
                    players_arr.append(str(len(userid)) + '. ' + profile.display_name)
                    print(players_arr)
                    players = '\n'.join(players_arr)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(str_curr + players))

                elif len(userid) > 0: # If players more than 0
                    if profile.user_id not in userid: # If he/she is a new player
                        userid.append(profile.user_id) 
                        displayname.append(profile.display_name)
                        print('Add user ID: ' + profile.user_id)    
                        line_bot_api.push_message(profile.user_id, TextSendMessage(msg_join))

                        # Announce who are the players
                        players_arr.append(str(len(userid)) + '. ' + profile.display_name)
                        print(players_arr)          
                        players = '\n'.join(players_arr)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(str_curr + players))
                    else:  # If not a new player
                        print('Not a new player')
                        line_bot_api.reply_message(event.reply_token, TextSendMessage('Sorry, you are already in the game'))

                print('PLAYERS: ' + str(players_arr))       

    #########################################################
    ######################################################### STATE 1
    #########################################################
    
    if incoming_msg == '/startgame' and state == 0: # Kasih role ke masing" orang, randomize depends on the num of players
        if isinstance(event.source, SourceGroup):
            if len(userid) >= 2 and len(userid) <= 6: # If total players antara 4-6
                state = 1
                groupid = event.source.group_id
                print('Game has started | 4-6 players')
                line_bot_api.reply_message(event.reply_token, TextSendMessage('The game has started!! \nAuuuuuuuwwww!! Who is the werewolf here? Let\'s find out!'))
            
                #################################################################### Giving the roles

                # Define data
                data = {'player': []}

                # Randomize roles for 4-6 players
                role = ['Werewolf', 'Seer']
                for y in range(len(userid)-2):
                    role.append('Villager')
                random.shuffle(role) 

                # Assign to dictionaries
                for x in range(len(userid)): # 0 - 3
                    each_data = {
                        "userid": userid[x],
                        "displayname": displayname[x],
                        "role": role[x],
                    }
                    data['player'].append(each_data)

                    # Define description for each role
                    if data['player'][x]['role'] == 'Werewolf':
                        role_desc = 'You can go WOLF TRIGGER and attack a player at night'
                    elif data['player'][x]['role'] == 'Seer':
                        role_desc = 'You can go STALKER TRIGGER at night to see a player\'s role'
                    elif data['player'][x]['role'] == 'Villager':
                        role_desc = 'You are useless'
                    else:
                        print('hmmm, ada error tuh..')

                    line_bot_api.push_message(data['player'][x]['userid'], TextSendMessage('Your role is: ' + data['player'][x]['role'] + '\n' + role_desc))

                print('Group ID: ' + groupid)
                print('UserID: ' + str(userid))
                print('Display name: ' + str(displayname))
                print('Role: ' + str(role))
                print('DATA: ' + str(data))
                # print(data['player'][0]['displayname'])
                # print(data['player'][3]['userid'])                

                #################################################################### Day & Night cycle begin

                while True:
                    # Night - Nocturnal phase
                    time.sleep(5)
                    line_bot_api.push_message(groupid, TextSendMessage('🌙 Malam telah tiba, \nSebagian telah tertidur kelelahan, sebagian mulai bersiap melancarkan aksinya. \nPemain malam hari: kalian punya 120 detik untuk menjalankan aksimu (ง•̀-•́)ง !!'))
                    
                    # kasih opsi(pm) ke werewolf sapa yg mw dibunuh berserta opsi tidak mw membunuh & kasih opsi(pm) ke seer sapa yg mw di liat roleny dgn waktu 120 detik(max) untuk kedua role tersebut

                    # Day - Announcement phase
                    time.sleep(5)
                    line_bot_api.push_message(groupid, TextSendMessage('🌤 Pagi telah tiba, oops ada yang mati neh.'))
                    # time.sleep(10) # kasih waktu 10 detik untuk orang liat (ekspresi kaget karna 1 villager mati)

                    # villager brkurang 1 pke try except
                    # check if villager == 0 -> end game (manggil function game over)
                    
                    # Noon - Discussion phase
                    time.sleep(5)
                    line_bot_api.push_message(groupid, TextSendMessage('☀️ Siang Hari. \nMatahari tepat di atas kepala. Warga desa mempunyai 150 detik untuk menuduh / membela diri / ngambek dituduh.. \nPokoknya damai lho ya \n(╭￣3￣)╭'))
                    
                    # kasih waktu 150 detik(not max) buat discuss, menuduh / membela diri dkk

                    # Afternoon - Vote phase
                    time.sleep(5)
                    line_bot_api.push_message(groupid, TextSendMessage('🌥 Senja telah tiba. \nSeluruh warga berkumpul di balai desa untuk memilih siapa yang akan dieksekusi, sebagian warga terlihat sibuk menyiapkan alat penyiksaan untuk malam ini. \nKalian mempunyai waktu selama 90 detik untuk memilih! \nSemua pemain yang masih hidup dapat kesempatan untuk memilih satu orang siapa yang akan dieksekusi.'))

                    # kasih opsi sapa yg mw di vote untuk dieksekusi dgn waktu 90 detik(max)
                    # player brkurang 1 pke try except
                    # stlh vote selesai, announce klo yg di vote mati and ksh time.sleep(10) untuk mreka liat (ekspresi kaget apakah itu bner ww ato villager)
                    # check if werewolf == 0 -> end game (manggil function game over)

                    # For testing only
                    if incomie_msg == 'stop':
                        break


            elif len(userid) >= 7 and len(userid) <= 12: # If total players antara 7-12
                state = 1
                print('Game has started | 7-12 players')
                line_bot_api.reply_message(event.reply_token, TextSendMessage('The game has started!! \nAuuuuuuuwwww!! Who are the werewolves here? Let\'s find out!'))
            elif len(userid) < 4: # If players kurang dari 4
                line_bot_api.reply_message(event.reply_token, TextSendMessage('Sorry, you are too lonely (min 4 ppl)'))
            elif len(userid) > 12:  # If players lebih dari 12
                line_bot_api.reply_message(event.reply_token, TextSendMessage('Sorry, you guys are too crowded (max 12 ppl)'))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage('Werewolf is under maintenance :)'))

    print('STATE: ' + str(state))

    # if incoming_msg == '/leave':
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage('See you next game, '))
    