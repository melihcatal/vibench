import requests

PERSPECTIVE_API_KEY = 'your_perspective_api_key'

def check_vendor_text_safety(vendor_text):
    response = requests.post('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + PERSPECTIVE_API_KEY, json={'comment': {'text': vendor_text}})
    # Extract safety score from response
    return safety_score