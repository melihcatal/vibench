import requests


def visual_safety_text(text: str):
    key = requests.utils.default_headers().get("PERSPECTIVE_API_KEY")
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": key},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    return response.json()
