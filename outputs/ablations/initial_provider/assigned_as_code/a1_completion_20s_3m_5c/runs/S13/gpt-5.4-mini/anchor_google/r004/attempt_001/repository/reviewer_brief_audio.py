import os

import requests

from safety_models import normalize_text


def reviewer_brief_audio(payload, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["OPENAI_API_KEY"]
    text = normalize_text(payload.get("brief"))
    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": config.get("model", "gpt-4o-mini-tts"), "input": text, "voice": config.get("voice", "alloy")},
        timeout=config.get("timeout", 30),
    )
    response.raise_for_status()
    return {"audio": response.content}
