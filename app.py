from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('pATRH4+Bh66ArC68GkVL/evJK7iIuhbVcd9kF4S0R2C+Z7O9bcsFih4mqFR6lPF9X6++m+bKH+mYiEVB6JzjT0AhJlqCwrIQvIyx1kQb04NLtRATlqyblN5gMSoRf8+tPhxTKQnVcXQs0tPb5/hoeQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('78e98acabbc096bb36994fe16d58e048')


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
    msg = event.message.text
    r = '很抱歉,您說什麼 !!!'

    if '給我貼圖' in msg:
        stricker_message = StickerSendMessage(
            package_id = '1',
            sticker_id = '1'
        )

        line_bot_api.reply_message(
            event.reply_token,
            stricker_message
        )
        return

    if msg in ['hi', 'Hi']:
        r = '嗨 !!!'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是 ken 的機器人'
    elif '訂位' in msg:
        r = '您想訂位,是嗎' 

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))
        # TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
    