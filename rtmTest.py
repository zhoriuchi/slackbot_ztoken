import os
import time
from slackclient import SlackClient

slack_token = os.environ["SLACK_BOT_API_TOKEN"]
sc = SlackClient(slack_token)

if sc.rtm_connect():
  while sc.server.connected is True:
        request = sc.rtm_read()
        print(request)
        time.sleep(1)
else:
    print("Connection Failed")
