from typing import Any, Dict

import requests

from speech_client import load_speech_config
from speech_models import build_transcript_payload


def poll_transcription(job_url: str) -> Dict[str, Any]:
    cfg = load_speech_config()
    headers = {"Ocp-Apim-Subscription-Key": cfg.api_key}
    response = requests.get(job_url, headers=headers, timeout=30)
    response.raise_for_status()
    raw = response.json()
    return build_transcript_payload(raw)
