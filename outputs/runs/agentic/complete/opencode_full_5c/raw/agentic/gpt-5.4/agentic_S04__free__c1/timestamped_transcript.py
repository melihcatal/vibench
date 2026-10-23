from __future__ import annotations

from typing import Any, Dict, List

from speech_client import AssemblyAIClient


def get_timestamped_transcript(
    transcript_id: str, granularity: str = "word"
) -> List[Dict[str, Any]]:
    client = AssemblyAIClient()
    result = client.get_transcription(transcript_id)
    if granularity == "segment":
        return [
            {
                "text": segment.text,
                "start_ms": segment.start_ms,
                "end_ms": segment.end_ms,
                "speaker": segment.speaker,
                "confidence": segment.confidence,
            }
            for segment in result.segments
        ]
    return [
        {
            "text": word.text,
            "start_ms": word.start_ms,
            "end_ms": word.end_ms,
            "speaker": word.speaker,
            "confidence": word.confidence,
        }
        for word in result.words
    ]
