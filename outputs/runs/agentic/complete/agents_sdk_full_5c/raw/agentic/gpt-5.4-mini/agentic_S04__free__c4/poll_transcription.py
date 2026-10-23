from __future__ import annotations

from typing import Any, Dict

from speech_client import SpeechClientFactory
from speech_models import normalize_transcript


def poll_transcription(transcription_id: str) -> Dict[str, Any]:
    client = SpeechClientFactory.create()
    result = client.audio.transcriptions.retrieve(transcription_id)
    normalized = normalize_transcript(result)
    return {"text": normalized.text, "segments": [segment.__dict__ for segment in normalized.segments], "raw": normalized.raw}
