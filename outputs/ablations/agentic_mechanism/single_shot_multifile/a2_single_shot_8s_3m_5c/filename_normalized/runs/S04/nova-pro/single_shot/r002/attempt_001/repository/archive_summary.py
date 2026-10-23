import os
import requests

def archive_summary(transcript):
    api_key = os.getenv('GOOGLE_CLOUD_SUMMARIZATION_API_KEY')
    url = 'https://language.googleapis.com/v1/documents:summarize?key=' + api_key
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': transcript
        },
        'summarize': {
            'length': 1
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()['summary']