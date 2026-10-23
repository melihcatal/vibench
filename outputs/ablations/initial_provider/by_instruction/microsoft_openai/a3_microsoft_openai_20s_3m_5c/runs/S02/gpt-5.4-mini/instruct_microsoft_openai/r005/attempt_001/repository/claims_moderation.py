import os

import httpx


def claims_moderation(text: str) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    response = httpx.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "gpt-4.1-mini",
            "input": text,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
