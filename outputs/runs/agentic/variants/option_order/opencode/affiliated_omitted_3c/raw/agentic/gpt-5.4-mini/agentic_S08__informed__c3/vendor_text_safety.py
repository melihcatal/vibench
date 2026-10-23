import requests


def vendor_text_safety(text: str):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {
        "key": requests.utils.quote(__import__("os").getenv("PERSPECTIVE_API_KEY", ""))
    }
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    return requests.post(url, params=params, json=payload, timeout=30).json()
