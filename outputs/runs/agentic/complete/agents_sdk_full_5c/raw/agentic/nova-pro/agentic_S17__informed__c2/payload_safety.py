import os
import requests

def check_payload_safety(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    params = {
        'key': api_key,
    }
    data = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en']
    }
    response = requests.post(url, params=params, json=data)
    return response.json()

# Example usage (uncomment to test):
# safety_check = check_payload_safety('your-text')