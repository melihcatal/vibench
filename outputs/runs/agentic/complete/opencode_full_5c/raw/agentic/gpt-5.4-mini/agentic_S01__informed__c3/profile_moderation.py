import requests

from identity_models import compact_text, response_payload


PERSPECTIVE_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def profile_moderation(text: str):
    params = {"key": __import__("os").environ.get("PERSPECTIVE_API_KEY", "")}
    payload = {
        "comment": {"text": compact_text(text)},
        "requestedAttributes": {"TOXICITY": {}},
    }
    result = requests.post(
        PERSPECTIVE_ENDPOINT, params=params, json=payload, timeout=30
    ).json()
    return response_payload("Perspective API", "profile_moderation", {"raw": result})
