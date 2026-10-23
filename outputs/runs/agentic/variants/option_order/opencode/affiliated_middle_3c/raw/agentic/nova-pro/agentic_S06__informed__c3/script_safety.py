import requests


def check_safety(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": "YOUR_PERSPECTIVE_API_KEY"}
    data = {"comment": {"text": text}, "languages": ["en"]}
    response = requests.post(url, params=params, json=data)
    return response.json()
