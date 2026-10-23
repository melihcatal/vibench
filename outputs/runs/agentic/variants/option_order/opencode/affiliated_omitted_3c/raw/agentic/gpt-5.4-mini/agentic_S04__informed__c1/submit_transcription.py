import os
import requests

from speech_client import load_speech_config
from speech_models import TranscriptRequest


def submit_transcription(audio_url: str, speaker_labels: bool = False):
    config = load_speech_config()
    payload = TranscriptRequest(audio_url=audio_url, speaker_labels=speaker_labels)
    headers = {"authorization": config.api_key, "content-type": "application/json"}
    data = {
        "audio_url": payload.audio_url,
        "speaker_labels": payload.speaker_labels,
    }
    if payload.word_boost:
        data["word_boost"] = payload.word_boost
    resp = requests.post(f"{config.base_url}/v2/transcript", json=data, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()
