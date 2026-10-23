import os
import requests

from speech_client import load_speech_config


def moderate_transcript(payload, config=None):
    cfg = load_speech_config(config)
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={"Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY', cfg.api_key)}", "Content-Type": "application/json"},
        json={"model": "omni-moderation-latest", "input": payload["text"]},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
