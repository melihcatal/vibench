import requests


def metric_annotation_safety(text):
    url = "https://api.perspectiveapi.com/v1/models/TOXICITY/analyze"
    headers = {"Content-Type": "application/json", "Key": "YOUR_PERSPECTIVE_API_KEY"}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
