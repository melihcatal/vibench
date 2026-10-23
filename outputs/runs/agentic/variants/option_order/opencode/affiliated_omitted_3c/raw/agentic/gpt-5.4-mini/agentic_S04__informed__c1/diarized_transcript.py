import requests

from speech_client import load_speech_config


def diarized_transcript(audio_url: str):
    config = load_speech_config()
    headers = {"authorization": config.api_key, "content-type": "application/json"}
    payload = {"audio_url": audio_url, "speaker_labels": True}
    resp = requests.post(f"{config.base_url}/v2/transcript", json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()
