import requests

def changeStatus(userid, text):
    # 自分以外のユーザーを変えるには有料Slackでadmin権限がないとだめ
    token = 'xoxp-336766408353-350464515125-465998012352-6fe1e53fbeff08f32f76a9c820918a01'

    r = requests.post('https://slack.com/api/users.profile.set', params = {
        'token': token,
        'user': userid,
        'profile': '{"status_text": "' + text + '", "status_emoji": ""}'
    })
