import requests
from security_models import safety_score_request

def payload_safety(text):
    payload = safety_score_request(text)
    response = requests.post('https://api.perspectiveapi.com/v1alpha1/comments:analyze', params={'key': __import__('os').environ.get('PERSPECTIVE_API_KEY','')}, json=payload, timeout=30)
    return response.json()
