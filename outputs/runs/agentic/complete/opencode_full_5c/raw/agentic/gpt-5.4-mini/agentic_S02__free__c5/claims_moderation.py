import os
from typing import Iterable

import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def moderate_claim_text(text: str) -> dict:
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={"model": "omni-moderation-latest", "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
