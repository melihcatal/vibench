import requests

def secret_label_safety(text):
    response = requests.post('https://api.perspectiveapi.com/v1/comment',
                             json={"comment": {"text": text}},
                             headers={"Authorization": "Bearer PERSPECTIVE_API_KEY"})
    return response.json()