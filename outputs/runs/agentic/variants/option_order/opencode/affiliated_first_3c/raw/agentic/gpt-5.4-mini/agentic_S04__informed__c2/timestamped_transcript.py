from typing import Any, Dict, List

import requests

from speech_client import load_speech_config
from speech_models import build_transcript_payload


def timestamped_transcript(job_url: str) -> List[Dict[str, Any]]:
    cfg = load_speech_config()
    headers = {"Ocp-Apim-Subscription-Key": cfg.api_key}
    response = requests.get(job_url, headers=headers, timeout=30)
    response.raise_for_status()
    payload = build_transcript_payload(response.json())
    return payload["segments"]
