import requests

def check_caption_safety(caption):
    api_key = 'YOUR_PERSPECTIVE_API_KEY'
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + api_key
    payload = {
        'comment': {'text': caption},
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(url, json=payload)
    return response.json()