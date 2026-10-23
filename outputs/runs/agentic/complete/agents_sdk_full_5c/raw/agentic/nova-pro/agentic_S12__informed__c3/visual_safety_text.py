import requests

def check_safety(text):
    api_url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    params = {
        'key': 'YOUR_PERSPECTIVE_API_KEY'
    }
    data = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(api_url, params=params, json=data)
    return response.json()['attributeScores']['TOXICITY']['summaryScore']['value']
