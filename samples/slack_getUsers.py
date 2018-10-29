import requests
import json
import os

#Slack設定
SLACK_URL = 'https://slack.com/api/users.list'
slack_token = os.environ["SLACK_BOT_API_TOKEN"]

payload = {'token':slack_token}
r = requests.get(SLACK_URL, params=payload)
#print(r.text)

#Convert to Dictionary
data = json.loads(r.text)
members = data['members']

for m in members:
	print(m['id'])
