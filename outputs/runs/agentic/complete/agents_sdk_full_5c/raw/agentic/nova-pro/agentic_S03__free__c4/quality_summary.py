import os
import requests

def quality_summary(text):
    url = 'https://api.meaningcloud.com/summarization-1.0'
    api_key = os.getenv('MEANINGCLOUD_API_KEY')
    params = {
        'key': api_key,
        'txt': text,
        'sentences': '3'
    }
    response = requests.post(url, params=params)
    return response.json()['summary']