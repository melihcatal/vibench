import os
from typing import Dict

import requests


def moderate_claim_text(text: str) -> Dict[str, object]:
    endpoint = "https://api.perspectiveapi.com/v1/comments:analyze"
    response = requests.post(
        endpoint,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
