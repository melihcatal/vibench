import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def is_unsafe(text):
    """Check text with Perspective API for toxicity."""
    if not PERSPECTIVE_API_KEY:
        raise RuntimeError("Set PERSPECTIVE_API_KEY env var")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    headers = {"key": PERSPECTIVE_API_KEY}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    score = resp.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return score > 0.8  # threshold for unsafe
