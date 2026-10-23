import requests


def check_safety(text: str):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/perspective/analyze"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
