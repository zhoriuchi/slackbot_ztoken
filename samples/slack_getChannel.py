import os
from slackclient import SlackClient

slack_token = os.environ["SLACK_BOT_API_TOKEN"]
sc = SlackClient(slack_token)

response = sc.api_call("channels.list")
print(response)
