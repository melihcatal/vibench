import requests

from document_client import require_env


def vendor_text_safety(text: str) -> dict:
    resp = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        params={"key": require_env("PERSPECTIVE_API_KEY")},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    return resp.json()
