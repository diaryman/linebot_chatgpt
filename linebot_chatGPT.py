from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import openai
openai.api_key = "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"
model_use = "text-davinci-003"

channel_secret = "653bf2cf1d71d23ae72c5b185ba9e84c"
channel_access_token = "OVFLcrVDVD+BtPeFS0Lf/nL2wF58rmlJcL51/K7M1TsL0u23uuqAZw9RxXFL6fpgo93x/k6jdFLtOUElDbG0xaKocxwFtVJldloAJH05FdyFemV/kqlg8An8vAoA5x9/VTjJAj8fzJFdZ2ipNeVLqAdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    print(text)

    prompt_text = text

    response = openai.Completion.create(
        model=model_use,
        prompt=prompt_text,  
        max_tokens=1024) # max 4096

    text_out = response.choices[0].text 
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=text_out))

if __name__ == "__main__":          
    app.run()

