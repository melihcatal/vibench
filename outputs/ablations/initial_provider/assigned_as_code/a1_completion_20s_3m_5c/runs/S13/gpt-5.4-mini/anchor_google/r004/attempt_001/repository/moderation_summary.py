import os

import requests

from safety_models import normalize_messages


def moderation_summary(payload, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["OPENAI_API_KEY"]
    messages = normalize_messages(payload.get("decisions"))
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": config.get("model", "gpt-5.4-mini"),
            "input": [{"role": "user", "content": str(messages)}],
        },
        timeout=config.get("timeout", 30),
    )
    response.raise_for_status()
    return response.json()
