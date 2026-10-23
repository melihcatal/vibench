import json

import requests


def moderate_claim_text(text: str) -> str:
    response = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        params={"key": __import__("os").getenv("PERSPECTIVE_API_KEY", "")},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=20,
    )
    return json.dumps(response.json())
