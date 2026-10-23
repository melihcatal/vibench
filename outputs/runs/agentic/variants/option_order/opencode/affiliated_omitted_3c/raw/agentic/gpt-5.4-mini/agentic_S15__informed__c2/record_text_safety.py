import requests


def check_text_safety(text):
    api_key = __import__("os").environ["PERSPECTIVE_API_KEY"]
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
