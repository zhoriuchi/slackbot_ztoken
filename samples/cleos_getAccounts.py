import os
import time
import json
import subprocess
from slackclient import SlackClient

#Alias setting for CLEOS
CLEOS = "docker exec -i eosio /opt/eosio/bin/cleos --wallet-url http://127.0.0.1:5555 -u https://jungle.eosio.cr:443 "

#CLEOS command
cmd = CLEOS + "get accounts EOS712dUcdRJSqNDYQ4jVMZqfTspZCKtxeQ1JnkHpDByeFKbeom8W"
res = subprocess.check_output(cmd.split())

#JSON convert
my_json = res.decode('utf8')
data = json.loads(my_json)
#print(data)

accounts = data['account_names']
for a in accounts:
	print(a)
