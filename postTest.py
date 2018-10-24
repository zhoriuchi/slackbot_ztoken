import os
from slackclient import SlackClient

slack_token = os.environ["SLACK_BOT_API_TOKEN"]
sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel="CDK2QH970",
  text="Hello from Python!",
  reply_broadcast=True
)
