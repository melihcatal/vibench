import os

import requests


def localized_audio_preview(payload, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ.get("OPENAI_API_KEY", "")
    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": "gpt-4o-mini-tts", "voice": config.get("voice", "alloy"), "input": payload["text"]},
        timeout=30,
    )
    response.raise_for_status()
    return {"audio": response.content}
