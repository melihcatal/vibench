from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import build_speech_client
from speech_models import TranscriptStatus, normalize_segments


def timestamped_transcript(transcript_id: str, granularity: str = "word") -> Dict[str, Any]:
    client = build_speech_client()
    transcript = TranscriptStatus.from_assemblyai(client.get_transcript(transcript_id))
    segments = normalize_segments(transcript, granularity=granularity)
    return {
        "provider": "AssemblyAI",
        "transcript_id": transcript.id,
        "status": transcript.status,
        "granularity": granularity,
        "timestamps": [
            {
                "text": item.text,
                "start_ms": item.start_ms,
                "end_ms": item.end_ms,
                "speaker": item.speaker,
                "confidence": item.confidence,
            }
            for item in segments
        ],
    }
