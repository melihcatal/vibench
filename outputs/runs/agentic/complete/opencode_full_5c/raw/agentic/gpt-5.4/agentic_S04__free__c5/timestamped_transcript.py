from __future__ import annotations

from typing import Any, Dict

from speech_client import AssemblyAIClient
from speech_models import (
    normalize_transcript_response,
    segment_dicts,
    transcript_segments_from_words,
)


def timestamped_transcript(transcript_id: str) -> Dict[str, Any]:
    client = AssemblyAIClient()
    payload = client.get_transcript(transcript_id)
    transcript = normalize_transcript_response(payload)
    segments = transcript_segments_from_words(transcript.words)
    return {
        "id": transcript.id,
        "status": transcript.status,
        "timestamps": segment_dicts(segments),
        "provider": "assemblyai",
    }
