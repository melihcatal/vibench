import requests


def visual_safety_text(text: str):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    payload = {'comment': {'text': text}, 'languages': ['en'], 'requestedAttributes': {'TOXICITY': {}}}
    resp = requests.post(url, params={'key': 'PERSPECTIVE_API_KEY'}, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()
