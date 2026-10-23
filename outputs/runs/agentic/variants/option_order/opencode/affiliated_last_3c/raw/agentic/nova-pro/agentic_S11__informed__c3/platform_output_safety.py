import requests


def check_safety(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/perspective/analyze"
    headers = {
        "Content-Type": "application/json",
        "API-Key": os.getenv("PERSPECTIVE_API_KEY"),
    }
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
