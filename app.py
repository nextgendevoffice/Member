from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import config

app = Flask(__name__)

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    user_id = event.source.user_id  # Get the user's LINE ID

    if text.startswith('/YiKi'):
        # Handle checking rounds and results
        pass
    elif text.startswith('/bet'):
        # Handle placing bets
        pass
    elif text.startswith('/history'):
        # Handle displaying betting history
        pass
    elif text.startswith('/redeem'):
        # Handle coupon redemption
        pass
    elif text.startswith('/withdraw'):
        # Handle credit withdrawal
        pass
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Invalid command'))

if __name__ == "__main__":
    app.run()
