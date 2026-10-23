from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import get_client, load_config
from speech_models import build_diarization_payload, normalize_transcript_response


def diarized_transcript(audio_path: str, *, speakers: int = 2, language: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    config = load_config()
    client = get_client(config)
    payload = build_diarization_payload(audio_path=audio_path, speakers=speakers, language=language or config.default_language, model=model or config.default_model)
    result = client.transcriptions.create(payload)
    return normalize_transcript_response(result)
