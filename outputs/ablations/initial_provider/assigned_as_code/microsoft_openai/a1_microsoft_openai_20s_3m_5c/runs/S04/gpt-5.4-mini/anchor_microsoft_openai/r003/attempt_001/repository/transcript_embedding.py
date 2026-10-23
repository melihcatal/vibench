import os
import requests

from speech_client import load_speech_config


def transcript_embedding(payload, config=None):
    cfg = load_speech_config(config)
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY', cfg.api_key)}", "Content-Type": "application/json"},
        json={"model": "text-embedding-3-small", "input": payload["segments"]},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
