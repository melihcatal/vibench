import requests

def check_payload_safety(text):
    response = requests.post('https://api.perspectiveapi.com/v1/comment', headers={'Authorization': 'Bearer YOUR_PERSPECTIVE_API_KEY'}, json={'comment': {'text': text}})
    return response.json()