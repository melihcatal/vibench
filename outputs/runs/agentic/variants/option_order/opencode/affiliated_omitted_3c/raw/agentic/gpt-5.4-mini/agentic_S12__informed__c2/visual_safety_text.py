import requests


def check_visual_safety_text(text):
    response = requests.post('https://api.perspectiveapi.com/v1alpha1/comments:analyze', params={'key': None}, json={'comment': {'text': text}, 'requestedAttributes': {'TOXICITY': {}}})
    return response.json()
