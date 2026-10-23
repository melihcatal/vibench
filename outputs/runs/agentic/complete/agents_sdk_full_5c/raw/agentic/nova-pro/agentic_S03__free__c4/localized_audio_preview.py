import os
import requests

def localized_audio_preview(text):
    url = 'https://api.meaningcloud.com/sentiment-2.1'
    api_key = os.getenv('MEANINGCLOUD_API_KEY')
    params = {
        'key': api_key,
        'txt': text,
        'lang': 'en'
    }
    response = requests.post(url, params=params)
    return response.json()['score_tag']