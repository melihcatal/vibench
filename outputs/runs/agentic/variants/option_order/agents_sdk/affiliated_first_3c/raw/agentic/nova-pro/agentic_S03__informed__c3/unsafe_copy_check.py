import requests

def check_unsafe_content(text):
    perspective_api_key = 'YOUR_PERSPECTIVE_API_KEY'
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + perspective_api_key
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
    }
    response = requests.post(url, json=payload)
    return response.json()