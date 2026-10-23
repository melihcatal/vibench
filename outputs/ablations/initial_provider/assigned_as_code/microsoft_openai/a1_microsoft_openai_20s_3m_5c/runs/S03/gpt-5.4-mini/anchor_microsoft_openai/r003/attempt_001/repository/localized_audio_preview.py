import requests

from translation_client import load_translation_config


def localized_audio_preview(payload, config=None):
    cfg = load_translation_config(config)
    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={"Authorization": f"Bearer {cfg.api_key}", "Content-Type": "application/json"},
        json={"model": "gpt-4o-mini-tts", "voice": payload["voice"], "input": payload["text"]},
        timeout=30,
    )
    response.raise_for_status()
    return {"audio": response.content, "voice": payload["voice"]}
