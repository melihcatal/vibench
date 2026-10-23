from __future__ import annotations

from speech_client import get_transcriber
from speech_models import normalize_assemblyai_transcript


def timestamped_transcript(transcript_id: str, level: str = "word") -> dict:
    transcriber = get_transcriber()
    transcript = transcriber.get_by_id(transcript_id)
    result = normalize_assemblyai_transcript(transcript)
    if level == "segment":
        timestamps = [
            {
                "text": segment.text,
                "speaker": segment.speaker,
                "start": segment.start,
                "end": segment.end,
            }
            for segment in result.segments
        ]
    else:
        raw_words = result.raw.get("words") or []
        timestamps = [
            {
                "text": word.get("text"),
                "start": round(word.get("start", 0) / 1000.0, 3),
                "end": round(word.get("end", 0) / 1000.0, 3),
                "confidence": word.get("confidence"),
            }
            for word in raw_words
        ]
    return {
        "transcript_id": result.transcript_id,
        "status": result.status,
        "timestamps": timestamps,
        "provider": "assemblyai",
    }
