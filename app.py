import pickle
import numpy as np

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter


SLACK_TOKEN = "xoxb-656725000466-731579237621-NEhqRSQjtDvS2oZ1PJyrOb0r"
SLACK_SIGNING_SECRET = "599d518ad04b54b6915dedf2c567c399"

app = Flask(__name__)

slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

# Req. 2-1-1. pickle로 저장된 model.clf 파일 불러오기
loaded_model = pickle.load(open("model.clf", 'rb'))
beta_0 = loaded_model.coef_[0][0]
beta_1 = loaded_model.coef_[0][1]
beta_2 = loaded_model.coef_[0][2]
beta_3 = loaded_model.intercept_[0]
# Req. 2-1-2. 입력 받은 광고비 데이터에 따른 예상 판매량을 출력하는 lin_pred() 함수 구현
def lin_pred(test_str):
    test_str = test_str.replace("<@UMHH16ZJ9> ","")

    arr = test_str.split(" ")
    tv = arr[0]
    rd = arr[1]
    newspaper = arr[2]

    rs = ((float(tv) * beta_0 ) + (float(rd) * beta_1) + (float(newspaper) * beta_2 + beta_3))
    return rs

# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    # print(channel)
    # print(text)

    keywords = lin_pred(text)
    slack_web_client.chat_postMessage(
        channel=channel,
        text=keywords
    )

@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"

if __name__ == '__main__':
    app.run()
