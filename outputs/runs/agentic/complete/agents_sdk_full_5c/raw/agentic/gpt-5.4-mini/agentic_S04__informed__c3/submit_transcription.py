from __future__ import annotations

from pathlib import Path
from typing import Optional

from speech_client import build_transcriber, load_config
from speech_models import TranscriptionRequest, TranscriptionResponse


def submit_transcription(audio_file: str, language_code: Optional[str] = None) -> TranscriptionResponse:
    cfg = load_config()
    request = TranscriptionRequest(audio_path=audio_file, language_code=language_code or cfg.language_code)
    transcriber = build_transcriber(cfg)
    result = transcriber.transcribe(Path(request.audio_path).as_posix())
    return TranscriptionResponse(job_id=getattr(result, "id", ""), status=getattr(result, "status", "submitted"), transcript=None, segments=None)
