from typing import Any, Dict

import requests


def moderate_claim_text(text: str) -> Dict[str, Any]:
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={"Authorization": f"Bearer {__import__('os').environ['OPENAI_API_KEY']}"},
        json={"model": "omni-moderation-latest", "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
