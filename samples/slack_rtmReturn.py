import os
import time
import subprocess
from slackclient import SlackClient

slack_token = os.environ["SLACK_BOT_API_TOKEN"]
sc = SlackClient(slack_token)

if sc.rtm_connect():
  while sc.server.connected is True:
        request = sc.rtm_read()

        for event in request:
            if 'user' in event:
#                if event['user'] == (対象ユーザのID) and event['type'] == 'message':
                if event['type'] == 'message':
                    print(request)

                    sc.api_call(
                        "chat.postMessage",
                        channel="CDK2QH970",
                        text=event['text'],
                        reply_broadcast=True
                    )
        time.sleep(1)
else:
    print("Connection Failed")
