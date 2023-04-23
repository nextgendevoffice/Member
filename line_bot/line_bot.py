from linebot import LineBotApi, WebhookHandler
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from database import mongodb

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Add your LINE@ event handling functions here
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.lower()
    user_id = event.source.user_id

    if text == "join":
        # Check if the user is already a member
        existing_member = mongodb.get_member(user_id)
        if existing_member:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="You are already a member.")
            )
        else:
            # Register the user as a member
            member_data = {"user_id": user_id}
            mongodb.add_member(member_data)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="You have successfully joined as a member!")
            )