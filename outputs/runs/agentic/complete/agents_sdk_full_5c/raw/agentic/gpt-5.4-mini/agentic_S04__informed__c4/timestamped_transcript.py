from typing import Any, Dict, List

from speech_client import configure_client
from speech_models import normalize_transcript_result


def timestamped_transcript(transcript_id: str) -> Dict[str, Any]:
    client = configure_client()
    transcript = client.get_by_id(transcript_id)
    normalized = normalize_transcript_result(transcript)
    timestamps: List[Dict[str, Any]] = []
    for segment in normalized.segments:
        timestamps.append(
            {
                "text": segment.text,
                "start": segment.start,
                "end": segment.end,
                "speaker": segment.speaker,
                "words": segment.words,
            }
        )
    return {
        "transcript_id": normalized.transcript_id,
        "timestamps": timestamps,
    }
