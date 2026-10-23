from __future__ import annotations

from typing import Any, Dict, List

from speech_client import get_transcription
from speech_models import normalize_words


def timestamped_transcript(transcript_id: str, level: str = "word") -> Dict[str, Any]:
    raw = get_transcription(transcript_id)
    if raw.get("status") != "completed":
        return {
            "provider": "AssemblyAI Transcripts API",
            "transcript_id": transcript_id,
            "status": raw.get("status"),
            "timestamps": [],
            "raw": raw,
        }

    if level == "segment":
        timestamps: List[Dict[str, Any]] = []
        for utterance in raw.get("utterances") or []:
            timestamps.append(
                {
                    "text": utterance.get("text", ""),
                    "start": utterance.get("start"),
                    "end": utterance.get("end"),
                    "speaker": utterance.get("speaker"),
                    "confidence": utterance.get("confidence"),
                }
            )
    else:
        timestamps = normalize_words(raw)

    return {
        "provider": "AssemblyAI Transcripts API",
        "transcript_id": transcript_id,
        "status": raw.get("status"),
        "timestamp_level": level,
        "timestamps": timestamps,
        "raw": raw,
    }
