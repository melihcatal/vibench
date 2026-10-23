import requests

from speech_models import normalize_transcript


def live_caption_safety(text: str):
    api_key = __import__("os").environ.get("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": normalize_transcript(text)},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(
        f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}",
        json=payload,
        timeout=30,
    )
    return response.json()
