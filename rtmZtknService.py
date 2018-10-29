import os
import time
import json
import subprocess
from slackclient import SlackClient

CLEOS = "docker exec -i eosio /opt/eosio/bin/cleos --wallet-url http://127.0.0.1:5555 -u https://jungle.eosio.cr:443 "

slack_token = os.environ["SLACK_BOT_API_TOKEN"]
#wallet_pass = os.environ["CLEOS_WALLET_PASS"]
wallet_pass = "PW5JrvdvBYYDsnphVy2NwRUQAffoZdysz5YSaDnqJQJhxJo3FsnPW"
ADMIN_PUBLIC_KEY = "EOS712dUcdRJSqNDYQ4jVMZqfTspZCKtxeQ1JnkHpDByeFKbeom8W"

sc = SlackClient(slack_token)
if sc.rtm_connect():
  while sc.server.connected is True:
        request = sc.rtm_read()

        for event in request:
            if 'user' in event:
                if event['type'] == 'message':
                    print(request)

                    # Unlock wallet 
                    cmd = CLEOS + "wallet unlock -n ztknwallet --password " + wallet_pass;
                    subprocess.call(cmd.split())

                    # Check if user's account exist
#                    cmd = CLEOS + "get accounts " + ADMIN_PUBLIC_KEY
#                    res = subprocess.Popen(cmd.split())
#                    print(res)

                    # Convert to EOS account
                    userid = event['user'].lower()
                    dst = userid.translate(str.maketrans('67890', 'fghij'))
                    account = "zcp"+dst

                    # Transfer ZTKN to user
                    cmd = CLEOS + 'push action kenichieosio transfer ' + "'" + '{"from":"kenichieosio", "to":' + '"' + account + '",' +' "quantity":"10.00 ZTKN", "memo":"slack message sent"}' + "'" + ' -p kenichieosio'
                    print(cmd)
                    subprocess.call(cmd, shell=True)

                    # Check the ZTKN balance of the user
                    cmd = CLEOS + 'get table kenichieosio ' + account + ' accounts'
                    res = subprocess.check_output(cmd.split())
                    print(res)

                    #JSON convert
                    my_json = res.decode('utf8')
                    data = json.loads(my_json)
                    print(data)
                    sltext = '<@'+event['user'] + '> ' + 'added: 10 ZTKN, ' + 'balance: ' + data['rows'][0]['balance']
                    sc.api_call(
                        "chat.postMessage",
                        channel=event['channel'],
                        text=sltext,
#                        thread_ts=event['ts'],
                        reply_broadcast=True
                    )

                elif event['type'] == 'reaction_added':
                    print(request)

                    if 'item_user' in event and not event['user'] == event['item_user']:

                        # Unlock wallet 
                        cmd = CLEOS + "wallet unlock -n ztknwallet --password " + wallet_pass;
                        subprocess.call(cmd.split())

                        # Check if user's account exist
    #                    cmd = CLEOS + "get accounts " + ADMIN_PUBLIC_KEY
    #                    res = subprocess.Popen(cmd.split())
    #                    print(res)

                        # Convert to EOS account
                        r_userid = event['user'].lower()
                        dst = r_userid.translate(str.maketrans('67890', 'fghij'))
                        r_account = "zcp"+dst

                        i_userid = event['item_user'].lower()
                        dst = i_userid.translate(str.maketrans('67890', 'fghij'))
                        i_account = "zcp"+dst

                        # Transfer ZTKN to users
                        cmd = CLEOS + 'push action kenichieosio transfer ' + "'" + '{"from":"kenichieosio", "to":' + '"' + r_account + '",' +' "quantity":"1.00 ZTKN", "memo":"slack reaction did"}' + "'" + ' -p kenichieosio'
                        print(cmd)
                        subprocess.call(cmd, shell=True)

                        cmd = CLEOS + 'push action kenichieosio transfer ' + "'" + '{"from":"kenichieosio", "to":' + '"' + i_account + '",' +' "quantity":"1.00 ZTKN", "memo":"slack reaction received"}' + "'" + ' -p kenichieosio'
                        print(cmd)
                        subprocess.call(cmd, shell=True)

                        # Check the ZTKN balance of the users
                        cmd = CLEOS + 'get table kenichieosio ' + r_account + ' accounts'
                        r_res = subprocess.check_output(cmd.split())
                        print(r_res)

                        cmd = CLEOS + 'get table kenichieosio ' + i_account + ' accounts'
                        i_res = subprocess.check_output(cmd.split())
                        print(i_res)

                        #JSON convert
                        my_json = r_res.decode('utf8')
                        r_data = json.loads(my_json)
                        print(r_data)

                        my_json = i_res.decode('utf8')
                        i_data = json.loads(my_json)
                        print(i_data)

                        sltext = '<@'+event['user'] + '> ' + 'added: 1 ZTKN, ' + 'balance: ' + r_data['rows'][0]['balance'] + '\n' + '<@'+event['item_user'] + '> ' 'added: 1 ZTKN, ' + 'balance: ' + i_data['rows'][0]['balance']
                        sc.api_call(
                            "chat.postMessage",
                            channel=event['item']['channel'],
                            text=sltext,
#                            thread_ts=event['ts'],
                            reply_broadcast=True
                        )
        time.sleep(1)
else:
    print("Connection Failed")


