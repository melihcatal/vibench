from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

from speech_client import SpeechServiceConfig, get_client
from speech_models import TranscriptionJobResponse, normalize_segments


def poll_transcription(job_id: str) -> TranscriptionJobResponse:
    config = SpeechServiceConfig.from_env()
    client: OpenAI = get_client(config)
    result: Dict[str, Any] = client.audio.transcriptions.get(job_id).model_dump()
    return TranscriptionJobResponse(
        job_id=str(result.get("id", job_id)),
        status=str(result.get("status", "completed")),
        transcript=result.get("text"),
        segments=normalize_segments(result.get("segments", [])),
        raw=result,
    )
