import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# นำเข้า handler ที่เขียนเอง
from handlers import handle_text_message

app = Flask(__name__)

# ตั้งค่า LINE Bot ผ่าน environment variables
line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# สร้าง handler สำหรับข้อความที่เป็น TextMessage
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    handle_text_message(event)

if __name__ == "__main__":
    app.run()
