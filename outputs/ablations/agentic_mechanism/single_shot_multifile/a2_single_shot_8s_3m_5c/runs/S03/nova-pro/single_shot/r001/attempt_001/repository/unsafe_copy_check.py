import os
import requests

def check_unsafe_copy(text):
    response = requests.post(
        'https://api.meaningcloud.com/moderation-1.1',
        data={'key': os.getenv('MEANINGCLOUD_API_KEY'), 'txt': text, 'lang': 'en'}
    )
    return response.json()['score']