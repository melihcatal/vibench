import os

import httpx


def consent_translate(text: str, target_language: str) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    response = httpx.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "gpt-4.1-mini",
            "input": f"Translate this identity-provider consent copy to {target_language}: {text}",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
