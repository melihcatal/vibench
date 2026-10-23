import os

import requests


def reviewer_brief_audio(payload, config=None):
    text = payload["text"] if isinstance(payload, dict) else str(payload)
    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={"Authorization": f"Bearer {((config or {}).get('api_key') or os.environ['OPENAI_API_KEY'])}", "Content-Type": "application/json"},
        json={"model": "gpt-4o-mini-tts", "voice": (config or {}).get("voice", "alloy"), "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.content
