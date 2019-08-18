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


app = Flask(__name__)
# get LINE_CHANNEL_ACCESS_TOKEN from your environment variable
line_bot_api = LineBotApi(config("LINE_CHANNEL_ACCESS_TOKEN", default=os.environ.get('LINE_ACCESS_TOKEN')))
# get LINE_CHANNEL_SECRET from your environment variable
handler = WebhookHandler(config("LINE_CHANNEL_SECRET", default=os.environ.get('LINE_CHANNEL_SECRET')))
access_token = config("LINE_CHANNEL_ACCESS_TOKEN")

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text                                
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    incoming_msg = event.message.text

    print('Income message: ' + incoming_msg)
    line_bot_api.reply_message(event.reply_token, TextSendMessage('Yo whatsup'))

    print('Testing..')

    msg_join = 'Congratulations!! You are joining the Werewolf Game'
    if incoming_msg == '/userid':
        if isinstance(event.source, SourceGroup):
            profile = line_bot_api.get_profile(event.source.user_id)
            print('Profile: ' + profile)
            userid = profile.user_id
            print(userid)
            print('Start sending to ' + profile.display_name)
            line_bot_api.push_message(userid, TextSendMessage(msg_join))





if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)