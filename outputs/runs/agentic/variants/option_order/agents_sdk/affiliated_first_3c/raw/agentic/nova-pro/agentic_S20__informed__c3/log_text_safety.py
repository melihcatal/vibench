import requests

def check_text_safety(text):
    response = requests.post(
        'https://api.perspectiveapi.com/v1/models/toxicity/classify',
        headers={'Authorization': 'Bearer YOUR_PERSPECTIVE_API_KEY'},
        json={'comment': {'text': text}}
    )
    return response.json()