from flask import Flask, request, abort
from line_bot.line_bot import line_bot_api, handler
from database import mongodb

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        abort(400)

    return 'OK'

# Add your LINE@ event handling functions and routing here

if __name__ == "__main__":
    app.run()
