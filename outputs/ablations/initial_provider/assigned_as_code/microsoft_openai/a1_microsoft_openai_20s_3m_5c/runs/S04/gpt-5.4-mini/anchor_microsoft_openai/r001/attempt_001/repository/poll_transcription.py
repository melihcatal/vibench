import os
import requests

from speech_client import load_speech_config, speech_endpoint
from speech_models import normalize_transcript


def poll_transcription(payload, config=None):
    cfg = load_speech_config(config)
    response = requests.get(
        speech_endpoint(cfg.region, f'speechtotext/transcriptions/{payload["job_id"]}'),
        params={'api-version': '2024-11-15'},
        headers={'Ocp-Apim-Subscription-Key': cfg.api_key},
        timeout=30,
    )
    response.raise_for_status()
    return normalize_transcript(response.json())
