import requests


def metric_annotation_safety(text):
    api_key = "YOUR_PERSPECTIVE_API_KEY"
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }
    response = requests.post(url, headers=headers, json=data, params={"key": api_key})
    return response.json()
