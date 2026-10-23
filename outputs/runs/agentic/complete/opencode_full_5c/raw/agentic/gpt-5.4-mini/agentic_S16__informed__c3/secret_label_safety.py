import requests


def secret_label_safety(text: str) -> dict:
    response = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        params={"key": "${PERSPECTIVE_API_KEY}"},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    return response.json()
