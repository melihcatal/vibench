import os
import requests

from speech_client import load_speech_config, speech_headers
from speech_models import normalize_transcript_response


def poll_transcription(job_id, config=None):
    cfg = load_speech_config(config)
    response = requests.get(
        f"https://{cfg.region}.api.cognitive.microsoft.com/speechtotext/transcriptions/{job_id}",
        params={"api-version": "2024-11-15"},
        headers=speech_headers(cfg.api_key),
        timeout=30,
    )
    response.raise_for_status()
    return normalize_transcript_response(response.json())
