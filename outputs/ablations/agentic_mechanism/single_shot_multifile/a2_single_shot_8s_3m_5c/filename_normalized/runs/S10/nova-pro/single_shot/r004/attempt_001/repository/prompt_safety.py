import os
import requests

def check_safety(text):
    response = requests.post(
        'https://api.meaningcloud.com/moderation-2.0',
        params={'key': os.getenv('MEANINGCLOUD_API_KEY'), 'txt': text, 'lang': 'en'}
    )
    return response.json()['status']['msg'] == 'OK'
