import requests


def secret_label_safety(api_key, text):
    url = "https://api.perspectiveapi.com/v1alpha1/commentAnalyzer"
    headers = {"Content-Type": "application/json", "API-Key": api_key}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
