from __future__ import annotations

from typing import Any, Dict, List, Optional

from speech_client import get_assemblyai_transcript
from speech_models import extract_segments, normalize_assemblyai_transcript


def timestamped_transcript(
    transcript_id: str,
    *,
    api_key: Optional[str] = None,
    granularity: str = "word",
) -> Dict[str, Any]:
    payload = get_assemblyai_transcript(transcript_id, api_key=api_key)
    job = normalize_assemblyai_transcript(payload)
    if granularity == "segment":
        segments = extract_segments(job, prefer_utterances=True)
        items = [
            {
                "text": segment.text,
                "start_ms": segment.start_ms,
                "end_ms": segment.end_ms,
                "speaker": segment.speaker,
                "confidence": segment.confidence,
            }
            for segment in segments
        ]
    else:
        items = [
            {
                "text": word.get("text"),
                "start_ms": word.get("start"),
                "end_ms": word.get("end"),
                "speaker": word.get("speaker"),
                "confidence": word.get("confidence"),
            }
            for word in (job.words or [])
        ]
    return {
        "provider": "assemblyai",
        "job_id": job.job_id,
        "status": job.status,
        "granularity": granularity,
        "timestamps": items,
    }
