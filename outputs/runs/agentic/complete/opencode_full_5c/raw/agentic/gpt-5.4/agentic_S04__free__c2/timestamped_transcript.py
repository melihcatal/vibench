from __future__ import annotations

from speech_client import ensure_completed, fetch_transcription


def timestamped_transcript(
    transcript_id: str, level: str = "word"
) -> dict[str, object]:
    result = ensure_completed(fetch_transcription(transcript_id))
    if level == "segment":
        segments = [
            {
                "start_ms": segment.start_ms,
                "end_ms": segment.end_ms,
                "text": segment.text,
                "speaker": segment.speaker,
            }
            for segment in result.segments
        ]
        return {
            "id": result.transcript_id,
            "status": result.status,
            "segments": segments,
        }

    words = result.raw.get("words") or []
    normalized_words = [
        {
            "text": word.get("text", ""),
            "start_ms": int(word.get("start", 0)),
            "end_ms": int(word.get("end", 0)),
            "confidence": word.get("confidence"),
            "speaker": word.get("speaker"),
        }
        for word in words
    ]
    return {
        "id": result.transcript_id,
        "status": result.status,
        "words": normalized_words,
    }
