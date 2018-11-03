import json
import re
from slackclient import SlackClient

#************************
# Get User StatusText and StatusEmoji1
#************************
def getStatus(token, userid):
    sc = SlackClient(token)
    res = sc.api_call("users.profile.get")
    if res['ok'] is False:
        return
    else:
        return res['profile']['status_text'], res['profile']['status_emoji']

#************************
# change User StatusText and StatusEmoji1
#************************
def changeStatus(token, userid, text):
    current_status = getStatus(token, userid)
    if current_status[1] == '':
        # 絵文字が空ならTextも空
        status_emoji = ':zcorp:'
        status_text  = text;
    else:
        status_emoji = current_status[1]
        if 'ZTKN' in current_status[0]:
            status_text =  re.sub(r'^.*ZTKN', text, current_status[0])
        else:
            status_text = text + ' ' + current_status[0]

    sc = SlackClient(token)
    sc.api_call("users.profile.set",
                user=userid,
                profile='{"status_text": "' + status_text + '", "status_emoji": "' + status_emoji + '"}'
    )
