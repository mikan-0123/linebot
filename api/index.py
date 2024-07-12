import logging
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    ButtonsTemplate, PostbackAction, TemplateSendMessage
)

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# LINE Botの設定
line_bot_api = LineBotApi('CtKyeXVni9YLGCzQ0AtFropS5/Pt0zpRjEXKyg3nV64ElwbTM2I/MUzK0zINJL+z3xdZY6dpC+Fj+yAHxE8+ztIaAxPqfbI0HiMN5jfo9aR+0aQjYuCzmzCuUHKEB6g8NOwMT2CUU47u3EkgRtQHCAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('db3558aee86828347970a145ff3bfca1')

# Webhookのエンドポイントを定義
@app.route("/api/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# メッセージイベントを処理するハンドラーを追加
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "投票":
        send_vote(event.reply_token)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="他のメッセージが送信されました。")
        )

    # グループIDを取得してログに出力
    group_id = event.source.group_id if event.source.type == 'group' else None
    if group_id:
        app.logger.info("Group ID: " + group_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="グループIDは " + group_id + " です。")
        )

# ボタンテンプレートを送信する関数
def send_vote(reply_token):
    buttons_template = ButtonsTemplate(
        title='サークル参加', text='どちらを選びますか？', actions=[
            PostbackAction(label='参加', data='action=vote&choice=1'),
            PostbackAction(label='不参加', data='action=vote&choice=2')
        ]
    )
    template_message = TemplateSendMessage(
        alt_text='投票です', template=buttons_template
    )
    line_bot_api.reply_message(reply_token, template_message)

if __name__ == "__main__":
    app.run(debug=True)
