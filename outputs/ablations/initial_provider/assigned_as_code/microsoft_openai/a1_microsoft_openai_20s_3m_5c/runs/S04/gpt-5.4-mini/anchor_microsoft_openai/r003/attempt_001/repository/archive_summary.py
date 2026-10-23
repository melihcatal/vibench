import os
import requests

from speech_client import load_speech_config


def archive_summary(payload, config=None):
    cfg = load_speech_config(config)
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY', cfg.api_key)}", "Content-Type": "application/json"},
        json={
            "model": "gpt-5.4-mini",
            "messages": [
                {"role": "system", "content": "Summarize transcription results concisely."},
                {"role": "user", "content": payload["text"]},
            ],
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
