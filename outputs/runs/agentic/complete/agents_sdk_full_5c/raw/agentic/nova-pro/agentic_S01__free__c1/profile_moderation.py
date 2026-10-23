import requests

def profile_moderation(text):
    API_KEY = os.getenv('PERSPECTIVE_API_KEY')
    URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    data = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(URL, params={'key': API_KEY}, json=data)
    return response.json()