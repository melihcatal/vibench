import requests

PERSPECTIVE_API_KEY = "your_perspective_api_key"


def claims_moderation(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {
        "key": PERSPECTIVE_API_KEY,
    }
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to moderate claims")
