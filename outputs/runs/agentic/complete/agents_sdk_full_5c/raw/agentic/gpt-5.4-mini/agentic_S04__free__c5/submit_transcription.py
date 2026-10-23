from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from openai import OpenAI

from speech_client import SpeechServiceConfig, get_client
from speech_models import TranscriptionJobRequest, TranscriptionJobResponse, normalize_segments


def submit_transcription(audio_file: str, *, language: Optional[str] = None, prompt: Optional[str] = None) -> TranscriptionJobResponse:
    config = SpeechServiceConfig.from_env()
    client: OpenAI = get_client(config)
    req = TranscriptionJobRequest(audio_path=audio_file, model=config.transcribe_model, language=language, prompt=prompt)
    with Path(req.audio_path).open("rb") as f:
        result: Dict[str, Any] = client.audio.transcriptions.create(
            model=req.model,
            file=f,
            language=req.language,
            prompt=req.prompt,
            response_format=req.response_format,
            include=req.include,
        ).model_dump()
    return TranscriptionJobResponse(
        job_id=str(result.get("id", result.get("job_id", ""))),
        status=str(result.get("status", "completed")),
        transcript=result.get("text"),
        segments=normalize_segments(result.get("segments", [])),
        raw=result,
    )
