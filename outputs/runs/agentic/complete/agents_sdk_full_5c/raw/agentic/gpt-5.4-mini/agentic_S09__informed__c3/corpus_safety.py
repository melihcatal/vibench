import requests


def corpus_safety(text: str) -> dict[str, object]:
    endpoint = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}},
    }
    api_key = __import__("os").environ.get("PERSPECTIVE_API_KEY", "")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required for Perspective API")
    response = requests.post(endpoint, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
