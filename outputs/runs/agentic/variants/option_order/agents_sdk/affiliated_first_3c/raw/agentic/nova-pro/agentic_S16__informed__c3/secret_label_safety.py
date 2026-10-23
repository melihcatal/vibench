import requests

def secret_label_safety(text):
    response = requests.post('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze', json={
        'comment': {'text': text},
        'languages': ['en']
    }, params={'key': 'YOUR_PERSPECTIVE_API_KEY'})
    return response.json()