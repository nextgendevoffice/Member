import re
from linebot import LineBotApi, WebhookHandler
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from database import mongodb
from config import ADMINS

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Add your LINE@ event handling functions here
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    user_id = event.source.user_id

    command = text.split(" ")[0].lower()

    if command == "/join":
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
    elif command == "/credit":
            credit = mongodb.get_credit(user_id)
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"Your current credit is: {credit}")
            )

    elif command == "/withdraw":
        amount = parse_amount(text)
        if amount:
            success, new_credit = mongodb.withdraw_credit(user_id, amount)
            if success:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"Withdrew {amount} credit. Your new balance is: {new_credit}")
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="Insufficient credit or invalid amount.")
                )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Invalid command format. Example: /withdraw 50")
            )
    elif user_id in ADMINS:
        
        if command == "/increase":
            target_user_id, amount = parse_user_and_amount(text)
            if target_user_id and amount:
                mongodb.adjust_credit(target_user_id, amount)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"Increased {amount} credit for user {target_user_id}.")
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="Invalid command format. Example: /increase USER_ID 50")
                )

        elif command == "/decrease":
            target_user_id, amount = parse_user_and_amount(text)
            if target_user_id and amount:
                mongodb.adjust_credit(target_user_id, -amount)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"Decreased {amount} credit for user {target_user_id}.")
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="Invalid command format. Example: /decrease USER_ID 50")
                )
    # Handle other text messages and commands...

def parse_amount(text):
    match = re.match(r"/withdraw (\d+(\.\d{1,2})?)", text)
    return float(match.group(1)) if match else None

def parse_user_and_amount(text):
    match = re.match(r"/(increase|decrease) (\w+) (\d+(\.\d{1,2})?)", text)
    return (match.group(2), float(match.group(3))) if match else (None, None)