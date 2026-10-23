import os
import requests


def moderate_claim_notes(text):
    resp = requests.post('https://api.perspectiveapi.com/v1alpha1/comments:analyze', params={'key': os.environ.get('PERSPECTIVE_API_KEY', '')}, json={'comment': {'text': text}, 'requestedAttributes': {'TOXICITY': {}}}, timeout=20)
    resp.raise_for_status()
    return resp.json()
