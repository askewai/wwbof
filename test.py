import random
import sys
import time
import pandas as pd

# ENDGAME
werewolf_win_msg = 'Congratulations WEREWOLF, YOU HAVE WON!!'
villager_win_msg = 'Congratulations VILLAGERS, YOU HAVE WON!!' 

def endgame_day(data, not_ww_index):
    # Check on day
    count = 0
    num_not_ww = len(not_ww_index)
    for c in range(num_not_ww): 
        if data[not_ww_index[c]['v_index']]['status'] == False: # Check if all villagers died
            count = count + 1   
            if count == num_not_ww-1:
                print(werewolf_win_msg) # pm group
                sys.exit()
                
def endgame_afternoon(data, not_ww_index, werewolf_index):
    # Check on noon
    count = 0
    num_not_ww = len(not_ww_index)
    for d in range(len(data)): # kalo 7-12 players beda logic
        if data[werewolf_index]['status'] == False: # Check if werewolf died
            print(villager_win_msg) # pm group
            sys.exit()
    
    for e in range(num_not_ww):
        if data[not_ww_index[e]['v_index']]['status'] == False: # Check if all villagers died
            count = count + 1
            if count == num_not_ww-1:
                print(werewolf_win_msg) # pm group
                sys.exit()
                
#############################################################
#############################################################

def startgame():
    userid = ['2312', '2141', '5252', '4910', '4829', '2949']
    displayname = ['KingBabelac', 'Buabelac', 'Itik', 'Cumi-Cuma', 'Lele', 'Babilac']
    # WW - Seer - Villager
    desc = ['You can eat any villagers', 'You can see the werewolf', '']
    data = []

    # Randomize roles for 4-6 players
    role = ['Werewolf', 'Seer']
    for y in range(len(userid)-2):
        role.append('Villager')
    random.shuffle(role) 

    for x in range(len(userid)): 
        each_data = {
            "userid": userid[x],
            "displayname": displayname[x],
            "role": role[x],
            "status": True
        }
        data.append(each_data)
    
    # print((data.keys()).index('2312'))
    print('Current data: ' + str(data))

    # Get Werewolf and Seer index
    for x in range(len(data)):
        if data[x]['role'] == 'Werewolf':
            werewolf_index = x # kalo 7 - 12 players pke array
        if data[x]['role'] == 'Seer':
            seer_index = x
    print('---------------------------------------------------------------------------')
    print('Werewolf Index: ' + str(werewolf_index))
    print('Seer Index: ' + str(seer_index))

    day_cycle(data, werewolf_index, seer_index)

#############################################################
#############################################################

def day_cycle(data, werewolf_index, seer_index):
    while True:
        # NIGHT
        # For Werewolf to choose who's going to be killed (PM)
        n = 0
        not_ww_index = []

        # for index ww # kalo 7 - 12 players
        # if not all false # # kalo 7 - 12 players
        print('===========================================================================')
        print('-- NIGHT --') # pm group
        print('HI ' + data[werewolf_index]['displayname'].upper() + ', You are the Werewolf!') # pm by userid
        for i,val in enumerate(data):
            if not val['role'] == 'Werewolf' and val['status'] == True: # Show all players who still alive except Werewolf
                n = n + 1
                not_ww_index.append(
                    {
                        'n': n,
                        'v_index': i
                    }
                )
                print(str(n) + '. ' + val['displayname']) # pm
                print(val)
                
        choice_to_kill = int(input('Pick your choices (WEREWOLF): ')) # pm
        print('Not WW Index: ' + str(not_ww_index))

        for k in range(len(not_ww_index)): # 0 - 4
            if choice_to_kill == not_ww_index[k]['n']:
                index_to_kill = not_ww_index[k]['v_index']
                player_killed = data[index_to_kill]['displayname']
                player_killed_role = data[index_to_kill]['role']
                print('---------------------------------------------------------------------------')
                print('YOU CHOOSE TO KILL ' + str(player_killed)) # pm       
                # data[index_to_kill]['status'] = False
                break
                
        # print('---------------------------------------------------------------------------')
        # print(data)

        #############################################################
        #############################################################

        # For Seer to pick who's going to be stalked (PM)
        n = 0
        not_seer_index = []
        
        if data[seer_index]['status'] == True: # Check if seer is still alive, else not pm him
            print('---------------------------------------------------------------------------')
            print('HI ' + data[seer_index]['displayname'].upper() + ', You are the Seer!') # pm by userid
            for i,val in enumerate(data):
                if not val['role'] == 'Seer' and val['status'] == True: # Show all players who still alive except Werewolf
                    n = n + 1
                    not_seer_index.append(
                        {
                            'n': n,
                            'p_index': i
                        }
                    )
                    print(str(n) + '. ' + val['displayname']) # pm
                    print(val)
                    
            choice_to_peek = int(input('Pick your choices (SEER): ')) # pm
            print('Not Seer Index: ' + str(not_seer_index))

            for k in range(len(not_seer_index)):
                if choice_to_peek == not_seer_index[k]['n']:
                    index_to_peek = not_seer_index[k]['p_index']
                    print('---------------------------------------------------------------------------')
                    print('YOU CHOOSE TO PEEK ' + str(data[index_to_peek]['displayname'] + '\n' + 'He/she is a ' + data[index_to_peek]['role'] + '!!')) # pm # print roleny dibuat bold # UNTUK 3 ROLES, FOR FURTHER VERSION, UPDATE THIS LINE
                    # player_stalked = data[index_to_peek]['displayname']
                    break
                
        #############################################################
        #############################################################
            
        # DAY - ANNOUNCEMENT PHASE
        # Announce pagi who's died last night
        print('===========================================================================')
        print('-- DAY --') # pm group
        data[index_to_kill]['status'] = False
        print('Pagi petang telah tiba, oops si ' + player_killed + ' mati!! Dia adalah ' + player_killed_role.upper() + '!!') # pm group
        print('---------------------------------------------------------------------------')
        print('Updated data (pagi): ' + str(data))

        # print('Check endgame function')
        time.sleep(2)
        endgame_day(data, not_ww_index) # CALL FUNCTION ENDGAME

        #############################################################
        #############################################################

        # NOON - DISCUSSION PHASE
        # time.sleep(150)
        print('===========================================================================')
        print('-- NOON --') # pm group
        print('Discuss guys!!') # pm group
        time.sleep(5)

        #############################################################
        #############################################################

        # AFTERNOON - VOTING PHASE
        print('===========================================================================')
        print('-- AFTERNOON --') # pm group
        print('Voting')
        n = 0
        not_dead_index = []
        
        for v,val in enumerate(data):
            if val['status'] == True:
                n = n + 1
                not_dead_index.append(
                    {
                        'n': n,
                        'a_index': v
                    }
                )
                print(str(n) + '. ' + val['displayname']) # pm group
                print(val)
                
        vote_input = int(input('Who are you guys going to vote? ')) # pm group ## CHECK THE MOST COUNTS IN THE VOTING 
        print('Not dead Index: ' + str(not_dead_index))
        
        for k in range(len(not_dead_index)):
            if vote_input == not_dead_index[k]['n']:
                index_to_executed = not_dead_index[k]['a_index']
                player_executed = data[index_to_executed]['displayname']
                player_executed_role = data[index_to_executed]['role']
                print('---------------------------------------------------------------------------')
                print('VOTE FOR ' + str(player_executed)) # pm group
                break

        # lele = [0 for k in range(len(not_dead_index))]
        # for k in range(len(not_dead_index)): # 0 - 3
        #     vote_input = int(input('Who are you guys going to vote? '))
        #     if data[not_dead_index[k]['a_index']]['userid'] 
            
        time.sleep(3) # time for reaction
        print(player_executed.upper() + ' EXECUTED!! HE/SHE IS ' + player_executed_role.upper() + '!!')
        data[index_to_executed]['status'] = False
            
        time.sleep(2)
        endgame_afternoon(data, not_ww_index, werewolf_index)

        #############################################################
        #############################################################

startgame()






