

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('7LhqZOkg0R5uKDdUzBsn0prhhTLQ0ebcv9z/Tdu5YSGvJ+hvYMS2UxOaOB3a6soxefagh5sG6q5bGSxfdPBJAmmjGvu5S68E5BbSLAQQ29dCE4xDBgmE1yJqP2NV3p5ROTC52jZTOXus+WcUs255XQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e958dcc939bd098c4083199566aa4a9f')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()