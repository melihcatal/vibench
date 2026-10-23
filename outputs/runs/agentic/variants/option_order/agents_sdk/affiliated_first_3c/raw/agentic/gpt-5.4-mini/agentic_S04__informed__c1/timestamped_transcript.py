from __future__ import annotations

from typing import Any, Dict

from speech_client import SpeechClientFactory
from speech_models import normalize_transcript_result


def timestamped_transcript(transcription_id: str) -> Dict[str, Any]:
    client = SpeechClientFactory.create()
    result = client.get_transcript(transcription_id)
    normalized = normalize_transcript_result(result)
    words = []
    for segment in normalized.segments:
        for word in segment.words or []:
            words.append(word)
    return {
        "id": transcription_id,
        "text": normalized.text,
        "timestamps": words,
        "segments": [segment.__dict__ for segment in normalized.segments],
    }
