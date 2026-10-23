import os
import requests

def check_corpus(text):
    response = requests.post(
        'https://api.meaningcloud.com/sentiment-2.1',
        data={'txt': text, 'key': os.getenv('MEANINGCLOUD_API_KEY')}
    )
    return response.json()['score_tag'] == 'P'