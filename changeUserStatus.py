import requests

def changeStatus(token, userid, text):
    # 自分以外のユーザーを変えるには有料Slackでadmin権限がないとだめ
    r = requests.post('https://slack.com/api/users.profile.set', params = {
        'token': token,
        'user': userid,
        'profile': '{"status_text": "' + text + '", "status_emoji": ""}'
    })
