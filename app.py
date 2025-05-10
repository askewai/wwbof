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
import game

app = Flask(__name__)

# get LINE_CHANNEL_ACCESS_TOKEN from your environment variable
line_bot_api = LineBotApi(config("LINE_CHANNEL_ACCESS_TOKEN", default=os.environ.get('LINE_ACCESS_TOKEN')))
# get LINE_CHANNEL_SECRET from your environment variable
handler = WebhookHandler(config("LINE_CHANNEL_SECRET", default=os.environ.get('LINE_CHANNEL_SECRET')))

@app.route("/callback", methods=['POST'])
def callback():
    # Ambil signature dari header request
    signature = request.headers.get('X-Line-Signature')

    # Ambil body dari request sebagai text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Menangani webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@app.route("/")
def home():
    return "Welcome to the Werewolf Bot!"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    incoming_msg = (event.message.text).lower()

    print('Income message: ' + incoming_msg)
    
    # Handling the 'menu' command
    if incoming_msg == 'menu':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="Here are the available commands:\n"
                     "/join - To join the game\n"
                     "/startgame - To start the game\n"
                     "/quit - To quit the game\n"
                     "bales dong - To make the bot reply 'knp ey?'\n"
                     "stop - To stop the game (for testing)"
            )
        )
    elif incoming_msg == 'bales dong':
        line_bot_api.reply_message(event.reply_token, TextSendMessage('knp ey?'))
    
    # Handling the 'quit' command to stop the game
    elif incoming_msg == '/quit':
        game.quit_game(event, line_bot_api, handler)
        line_bot_api.reply_message(event.reply_token, TextSendMessage('The game has been quit.'))

    # Call main game function
    game.main(event, line_bot_api, handler, incoming_msg)


if __name__ == "__main__":
    # Menggunakan port dari environment variable jika ada, jika tidak default ke 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
