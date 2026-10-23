import os

import requests

from safety_client import get_model


def moderation_summary(payload, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["OPENAI_API_KEY"]
    model = get_model(config, default="gpt-5.4-mini")
    response = requests.post("https://api.openai.com/v1/responses", headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json={"model": model, "input": payload.get("text", payload), "max_output_tokens": 120}, timeout=60)
    response.raise_for_status()
    return {"summary": response.json().get("output_text", "")}
