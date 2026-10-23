import requests
from model_models import normalize_text


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def prompt_safety(text: str):
    payload = {
        "comment": {"text": normalize_text(text)},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    resp = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": __import__("os").getenv("PERSPECTIVE_API_KEY", "")},
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()
