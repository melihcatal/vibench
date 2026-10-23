import requests


def unsafe_copy_check(text: str) -> dict:
    endpoint = 'https://api.perspectiveapi.com/v1alpha1/comments:analyze'
    params = {'key': __import__('os').environ.get('PERSPECTIVE_API_KEY', '')}
    payload = {'comment': {'text': text}, 'languages': ['en'], 'requestedAttributes': {'TOXICITY': {}}}
    response = requests.post(endpoint, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
