
def main(): # 4 - 6 players
    msg_join = 'Congratulations!! You are joining the Werewolf Game'
    if incoming_msg == '/join':
        if isinstance(event.source, SourceGroup):
            userid = []
            profile = line_bot_api.get_profile(event.source.user_id)
            userid.append(profile.user_id)
            print('User ID: ' + userid)
            print('Start sending to ' + profile.display_name)
            line_bot_api.push_message(userid, TextSendMessage(msg_join))
            
            if incoming_msg == '/startgame':
