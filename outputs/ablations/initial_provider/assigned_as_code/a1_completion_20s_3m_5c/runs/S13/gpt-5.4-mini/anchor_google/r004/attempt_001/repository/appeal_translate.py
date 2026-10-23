import os

import requests

from safety_models import normalize_text


def appeal_translate(payload, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["OPENAI_API_KEY"]
    text = normalize_text(payload.get("text"))
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": config.get("model", "gpt-5.4-mini"),
            "input": [{"role": "user", "content": f"Translate for moderation review: {text}"}],
        },
        timeout=config.get("timeout", 30),
    )
    response.raise_for_status()
    return response.json()
