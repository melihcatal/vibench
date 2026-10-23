import requests


def visual_safety_text(text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    headers = {"Content-Type": "application/json", "API-Key": api_key}
    response = requests.post(url, json=data, headers=headers)
    return response.json()
