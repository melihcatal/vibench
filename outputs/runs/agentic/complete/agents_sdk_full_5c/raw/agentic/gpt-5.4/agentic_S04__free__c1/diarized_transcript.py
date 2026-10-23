from __future__ import annotations

from typing import Any, Dict, List, Optional

from speech_client import submit_assemblyai_transcript
from speech_models import extract_segments, normalize_assemblyai_transcript


def request_diarized_transcript(
    audio_url: str,
    *,
    api_key: Optional[str] = None,
    language_code: Optional[str] = None,
) -> Dict[str, Any]:
    payload = submit_assemblyai_transcript(
        audio_url,
        api_key=api_key,
        language_code=language_code,
        speech_model="best",
        speaker_labels=True,
    )
    job = normalize_assemblyai_transcript(payload)
    segments = extract_segments(job, prefer_utterances=True)
    return {
        "provider": "assemblyai",
        "job_id": job.job_id,
        "status": job.status,
        "speaker_labels": True,
        "segments": [
            {
                "speaker": segment.speaker,
                "text": segment.text,
                "start_ms": segment.start_ms,
                "end_ms": segment.end_ms,
            }
            for segment in segments
        ],
    }
