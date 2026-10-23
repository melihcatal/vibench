from __future__ import annotations

from typing import Any, Dict, List

from speech_client import assemblyai_get
from speech_models import normalize_assemblyai_transcript


def timestamped_transcript(
    transcript_id: str, granularity: str = "word"
) -> Dict[str, Any]:
    payload = assemblyai_get(f"/transcript/{transcript_id}")
    normalized = normalize_assemblyai_transcript(payload)
    if granularity == "segment":
        timestamps: List[Dict[str, Any]] = [
            {
                "text": segment.text,
                "start": segment.start,
                "end": segment.end,
                "speaker": segment.speaker,
                "confidence": segment.confidence,
            }
            for segment in normalized.segments
        ]
    else:
        timestamps = [
            {
                "text": word.text,
                "start": word.start,
                "end": word.end,
                "speaker": word.speaker,
                "confidence": word.confidence,
            }
            for segment in normalized.segments
            for word in segment.words
        ]
    return {
        "provider": "AssemblyAI",
        "transcript_id": normalized.transcript_id,
        "status": normalized.status,
        "granularity": granularity,
        "timestamps": timestamps,
    }
