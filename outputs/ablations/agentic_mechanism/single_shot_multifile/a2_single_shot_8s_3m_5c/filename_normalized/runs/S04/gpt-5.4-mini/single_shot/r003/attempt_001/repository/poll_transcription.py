from __future__ import annotations

from typing import Any, Dict

from speech_client import get_client, load_config
from speech_models import normalize_transcript_response


def poll_transcription(transcription_id: str) -> Dict[str, Any]:
    config = load_config()
    client = get_client(config)
    result = client.transcriptions.get(transcription_id)
    return normalize_transcript_response(result)
