import requests

from speech_client import speech_client_config


def live_caption_safety(payload, config=None):
    config = speech_client_config(config)
    response = requests.post(
        f"{config['safety_endpoint']}/contentsafety/text:analyze?api-version=2024-09-01",
        headers={"api-key": config["api_key"], "Content-Type": "application/json"},
        json={"text": payload["text"]},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
