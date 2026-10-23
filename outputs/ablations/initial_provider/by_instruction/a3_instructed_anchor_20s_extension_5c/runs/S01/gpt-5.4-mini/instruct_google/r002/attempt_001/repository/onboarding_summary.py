import os

import requests

from identity_models import LifecycleResponse


def onboarding_summary(text: str):
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return LifecycleResponse(ok=False, error="missing_openai_api_key")
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": "gpt-5.4-mini",
            "messages": [{"role": "system", "content": "Summarize onboarding state for support."}, {"role": "user", "content": text}],
            "temperature": 0,
        },
        timeout=30,
    )
    if response.ok:
        return LifecycleResponse(ok=True, data=response.json())
    return LifecycleResponse(ok=False, error=response.text)
