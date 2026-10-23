import requests


def check_safety(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": "your_api_key"}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, params=params, json=data)
    return response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"] > 0.5
