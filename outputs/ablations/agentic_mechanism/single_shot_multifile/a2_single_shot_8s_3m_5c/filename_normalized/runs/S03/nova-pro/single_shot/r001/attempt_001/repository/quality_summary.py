import os
import requests

def summarize_quality(text):
    response = requests.post(
        'https://api.meaningcloud.com/summarization-1.0',
        data={'key': os.getenv('MEANINGCLOUD_API_KEY'), 'txt': text,'sentences': '3'}
    )
    return response.json()['summary']