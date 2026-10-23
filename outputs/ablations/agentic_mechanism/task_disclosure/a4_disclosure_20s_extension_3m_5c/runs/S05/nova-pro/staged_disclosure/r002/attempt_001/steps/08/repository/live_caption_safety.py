import os
import json
import requests

API_KEY = os.getenv('PERSPECTIVE_API_KEY')
ANALYZE_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

def check_unsafe_content(text):
    data = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {}, 'PROFANITY': {}}
    }
    headers = {
        'Content-Type': 'application/json'
    }
    params = {
        'key': API_KEY
    }
    response = requests.post(ANALYZE_URL, data=json.dumps(data), headers=headers, params=params)
    result = response.json()
    return result

if __name__ == '__main__':
    transcript_text = 'Sample transcript text to check for unsafe content.'
    result = check_unsafe_content(transcript_text)
    print(json.dumps(result, indent=2))