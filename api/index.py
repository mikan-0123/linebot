import logging

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "投票":
        send_vote(event.reply_token)

    # グループIDを取得してログに出力
    group_id = event.source.group_id if event.source.type == 'group' else None
    if group_id:
        app.logger.info("Group ID: " + group_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="グループIDは " + group_id + " です。")
        )

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
