import requests


def visual_safety_text(text: str):
    api_key = requests.utils.default_headers().get("PERSPECTIVE_API_KEY")
    resp = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=60,
    )
    return resp.json()
