import requests


def moderate_transcript(text):
    url = "https://api.perspectiveapi.com/v1/comment?key=PERSPECTIVE_API_KEY"
    data = {"comment": {"text": text}}
    response = requests.post(url, json=data)
    return response.json()
