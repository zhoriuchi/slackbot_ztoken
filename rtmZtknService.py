import os
import time
import json
import subprocess
import changeUserStatus
from slackclient import SlackClient

CLEOS = "docker exec -i eosio /opt/eosio/bin/cleos --wallet-url http://127.0.0.1:5555 -u https://jungle.eosio.cr:443 "

slack_token = os.environ["SLACK_BOT_API_TOKEN"]
slack_oauth_token = os.environ["SLACK_OAUTH_API_TOKEN"]
wallet_pwd = os.environ["CLEOS_WALLET_PASS"]
ADMIN_PUBLIC_KEY = "EOS712dUcdRJSqNDYQ4jVMZqfTspZCKtxeQ1JnkHpDByeFKbeom8W"

#Reward volume settings
REWARD_POST_MESSAGE = "10.00 ZTKN"
REWARD_REPLY_MESSAGE = "5.00 ZTKN"
REWARD_REACTION = "1.00 ZTKN"

#List for keeping EOS accounts
eos_accounts = []

#************************
# Get EOS accounts
#************************
def get_EOS_accounts():
    #CLEOS command
    cmd = CLEOS + "get accounts " + ADMIN_PUBLIC_KEY
    res = subprocess.check_output(cmd.split())

    #JSON convert
    my_json = res.decode('utf8')
    data = json.loads(my_json)

    accounts = data['account_names']
#    for a in eos_accounts:
#        print(a)
    return accounts

#************************
# Transfer "reward"(token) to the "account"
#************************
def transfer_token(account, reward):
    if account in eos_accounts:
        cmd = CLEOS + 'push action kenichieosio transfer ' + "'" + '{"from":"kenichieosio", "to":' + '"' + account + '",' +' "quantity":"' + reward + '", "memo":"slack message sent"}' + "'" + ' -p kenichieosio'
        print(cmd)
        subprocess.call(cmd, shell=True)
    else:
        pass #ToDo:エラー通知を送りたい

#************************
# Get Token balance of the account
#************************
def get_Token_balance(account):
    cmd = CLEOS + 'get table kenichieosio ' + account + ' accounts'
    res = subprocess.check_output(cmd.split())
    print(res)

    #JSON convert
    my_json = res.decode('utf8')
    data = json.loads(my_json)
    print(data)

    return data['rows'][0]['balance']

#************************
# Main
#************************
sc = SlackClient(slack_token)
if sc.rtm_connect():

    eos_accounts = get_EOS_accounts()

    while sc.server.connected is True:
        request = sc.rtm_read()
        for event in request:
            if 'user' in event:
                if event['type'] == 'message':
#                    print(request)

                    # Unlock wallet 
                    cmd = CLEOS + "wallet unlock -n ztknwallet --password " + wallet_pwd;
                    subprocess.call(cmd.split())

                    # Convert to EOS account
                    userid = event['user'].lower()
                    dst = userid.translate(str.maketrans('67890', 'fghij'))
                    account = "zcp"+dst

                    # Transfer ZTKN to user
                    if 'thread_ts' in event:
                        reward = REWARD_REPLY_MESSAGE
                    else:
                        reward = REWARD_POST_MESSAGE

                    transfer_token(account, reward)

                    # Get the ZTKN balance of the user
                    balance = get_Token_balance(account)

                    # Post a message to slack channel
                    sltext = '<@'+event['user'] + '> ' + 'added: ' + reward + ', ' + 'balance: ' + balance
                    sc.api_call(
                        "chat.postMessage",
                        #"chat.postEphemeral",
                        #user=event['user'],
                        #channel=event['channel'],
                        channel=event['user'],
                        text=sltext,
                        #thread_ts=event['ts'],
                        #reply_broadcast=True
                    )

                    changeUserStatus.changeStatus(slack_oauth_token, event['user'], balance)
                elif event['type'] == 'reaction_added':
                    print(request)

                    if 'item_user' in event and not event['user'] == event['item_user']:

                        # Unlock wallet 
                        cmd = CLEOS + "wallet unlock -n ztknwallet --password " + wallet_pwd;
                        subprocess.call(cmd.split())

                        # Convert to EOS account
                        r_userid = event['user'].lower()
                        dst = r_userid.translate(str.maketrans('67890', 'fghij'))
                        r_account = "zcp"+dst

                        i_userid = event['item_user'].lower()
                        dst = i_userid.translate(str.maketrans('67890', 'fghij'))
                        i_account = "zcp"+dst

                        # Transfer ZTKN to users
                        reward = REWARD_REACTION
                        transfer_token(r_account, reward)

                        reward = REWARD_REACTION
                        transfer_token(i_account, reward)

                        # Get the ZTKN balance of the user
                        r_balance = get_Token_balance(r_account)

                        # Get the ZTKN balance of the user
                        i_balance = get_Token_balance(i_account)

                        # Post a message to slack channel
                        sltext = '<@'+event['user'] + '> ' + 'added: ' + reward + 'balance: ' + r_balance + '\n' + '<@'+event['item_user'] + '> ' 'added: ' + reward + 'balance: ' + i_balance
                        sc.api_call(
                            "chat.postMessage",
                            #"chat.postEphemeral",
                            #user=event['user'],
                            #channel=event['channel'],
                            channel=event['user'],
                            text=sltext,
                            #thread_ts=event['ts'],
                            #reply_broadcast=True
                        )

                        changeUserStatus.changeStatus(slack_oauth_token, event['user'], r_balance)
                        changeUserStatus.changeStatus(slack_oauth_token, event['user'], i_balance)
        time.sleep(1)
else:
    print("Connection Failed")


