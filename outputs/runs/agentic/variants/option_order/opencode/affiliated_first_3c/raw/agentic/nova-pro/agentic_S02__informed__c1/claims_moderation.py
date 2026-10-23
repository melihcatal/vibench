import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def claims_moderation(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(
        url, headers=headers, params={"key": PERSPECTIVE_API_KEY}, json=payload
    )
    return response.json()
