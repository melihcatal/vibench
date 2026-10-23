import os

import requests

from safety_client import get_tts_voice


def reviewer_brief_audio(payload, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["OPENAI_API_KEY"]
    voice = get_tts_voice(config, default="alloy")
    text = payload.get("text", payload) if isinstance(payload, dict) else payload
    response = requests.post("https://api.openai.com/v1/audio/speech", headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json={"model": "gpt-4o-mini-tts", "voice": voice, "input": text}, timeout=60)
    response.raise_for_status()
    return {"audio": response.content, "voice": voice, "model": "gpt-4o-mini-tts"}
