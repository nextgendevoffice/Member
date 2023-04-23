from linebot.models import MessageEvent, TextMessage, TextSendMessage
from mongodb import collection
from app import line_bot_api

def handle_text_message(event):
    user_id = event.source.user_id
    text = event.message.text

    if text.lower() == "เครดิต":
        user_credit = collection.find_one({"user_id": user_id})
        if not user_credit:
            user_credit = {"user_id": user_id, "credits": 0}
            collection.insert_one(user_credit)
        
        reply_text = f"เครดิตของคุณคือ: {user_credit['credits']}"

    else:
        reply_text = "ขออภัย ฉันไม่เข้าใจคำสั่ง"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )
