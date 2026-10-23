from __future__ import annotations

from typing import Any, Dict, List

from poll_transcription import poll_transcription


def timestamped_transcript(
    transcript_id: str, granularity: str = "word"
) -> List[Dict[str, Any]]:
    result = poll_transcription(transcript_id)
    if granularity == "segment":
        return [
            {
                "text": segment.text,
                "start": segment.start,
                "end": segment.end,
                "speaker": segment.speaker,
                "confidence": segment.confidence,
            }
            for segment in (result.utterances or result.segments)
        ]
    items: List[Dict[str, Any]] = []
    for segment in result.utterances or result.segments:
        for word in segment.words:
            items.append(word)
    return items
