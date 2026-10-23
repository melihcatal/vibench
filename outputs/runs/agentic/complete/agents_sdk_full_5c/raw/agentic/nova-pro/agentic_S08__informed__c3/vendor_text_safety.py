import requests

def vendor_text_safety(vendor_text):
    response = requests.post('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=YOUR_PERSPECTIVE_API_KEY', json={'comment': {'text': vendor_text}, 'requestedAttributes': {'TOXICITY': {}}})
    return response.json()