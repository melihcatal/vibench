import requests


def visual_safety_text(text):
    api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": "your-perspective-api-key"}
    data = {"comment": {"text": text}, "languages": ["en"]}
    response = requests.post(api_url, params=params, json=data)
    return response.json()
