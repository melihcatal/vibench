import requests


def vendor_text_safety(text: str):
    api_key = __import__("os").environ.get("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    params = {"key": api_key}
    response = requests.post(url, json=payload, params=params, timeout=30)
    return response.json()
