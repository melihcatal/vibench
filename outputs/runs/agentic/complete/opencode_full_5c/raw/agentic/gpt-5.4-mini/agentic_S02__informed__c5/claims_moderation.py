import requests


def moderate_claim_text(text: str) -> dict:
    response = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        params={"key": __import__("os").environ.get("PERSPECTIVE_API_KEY", "")},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()
