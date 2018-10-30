import requests
import json
import os
import subprocess

#Slack settings
SLACK_URL = 'https://slack.com/api/users.list'
slack_token = os.environ["SLACK_BOT_API_TOKEN"]

#Alias setting for CLEOS
CLEOS = "docker exec -i eosio /opt/eosio/bin/cleos --wallet-url http://127.0.0.1:5555 -u https://jungle.eosio.cr:443 "

#EOS settings
wallet_pwd = os.environ["CLEOS_WALLET_PASS"]
ADMIN_PUBLIC_KEY = "EOS712dUcdRJSqNDYQ4jVMZqfTspZCKtxeQ1JnkHpDByeFKbeom8W"

#************************
# Get Slack users
#************************
#Slack API call
payload = {'token':slack_token}
r = requests.get(SLACK_URL, params=payload)
#print(r.text)

#Convert to Dictionary
data = json.loads(r.text)
members = data['members']
#for m in members:
#	print(m['id'])

#Convert to lower string and Translate restricted character to available one
# to follow EOS account restriction below
#
# EOS Account names must conform to the following guidelines:
# -Must be less than 13 characters
# -Can only contain the following symbols: .12345abcdefghijklmnopqrstuvwxyz
slack_accounts = []
account_list = []
for m in members:
	userid = m['id'].lower()
	dst = userid.translate(str.maketrans('67890', 'fghij'))
	account = "zcp"+dst
	slack_accounts.append(account)
	account_list.append([m['id'], account])

#Save to log file
print(account_list)
f = open('accountlog.txt', 'w')
for x in account_list:
    f.write(str(x) + "\n")
f.close()

#************************
# Get EOS accounts
#************************
#CLEOS command
cmd = CLEOS + "get accounts " + ADMIN_PUBLIC_KEY
res = subprocess.check_output(cmd.split())

#JSON convert
my_json = res.decode('utf8')
data = json.loads(my_json)

eos_accounts = data['account_names']
for a in eos_accounts:
	print(a)

#************************
# Create EOS account if not exist
#************************
# Unlock wallet 
cmd = CLEOS + "wallet unlock -n ztknwallet --password " + wallet_pwd;
subprocess.call(cmd.split())

for a in slack_accounts:
	if a not in eos_accounts:
		print(a)
		cmd = CLEOS + 'system newaccount --stake-net "1.0000 EOS" --stake-cpu "1.0000 EOS" --buy-ram-bytes 4096 kenichieosio ' + a + ' ' + ADMIN_PUBLIC_KEY + ' ' + ADMIN_PUBLIC_KEY
#		print(cmd)
		subprocess.call(cmd, shell=True)
