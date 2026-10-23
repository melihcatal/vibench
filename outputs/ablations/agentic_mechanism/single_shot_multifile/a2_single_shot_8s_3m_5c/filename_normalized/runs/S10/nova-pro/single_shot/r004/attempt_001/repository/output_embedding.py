import os
import requests

def embed_text(text):
    response = requests.post(
        'https://api.meaningcloud.com/sentiment-2.1',
        params={'key': os.getenv('MEANINGCLOUD_API_KEY'), 'txt': text, 'lang': 'en'}
    )
    return response.json()['score_tag']
