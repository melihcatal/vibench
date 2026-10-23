import requests


def moderate_transcript(text: str):
    api_key = __import__("os").environ.get("PERSPECTIVE_API_KEY", "")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    resp = requests.post(f"{url}?key={api_key}", json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()
