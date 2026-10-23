import os

import requests

from identity_models import LifecycleResponse


def profile_moderation(text: str):
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return LifecycleResponse(ok=False, error="missing_openai_api_key")
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": "omni-moderation-latest", "input": text},
        timeout=30,
    )
    if response.ok:
        return LifecycleResponse(ok=True, data=response.json())
    return LifecycleResponse(ok=False, error=response.text)
