from __future__ import annotations

import os
from typing import Any, Dict, Optional

from speech_client import get_client, resolve_audio_input
from speech_models import TranscriptionRequest, TranscriptionSubmission


def submit_transcription(audio_path: str, *, language: Optional[str] = None, model: Optional[str] = None, webhook_url: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    client = get_client()
    audio_source = resolve_audio_input(audio_path)
    request = TranscriptionRequest(audio_source=audio_source, language=language, model=model, webhook_url=webhook_url, metadata=metadata)
    submission = client.transcriptions.submit(request)
    if isinstance(submission, TranscriptionSubmission):
        return submission.to_dict()
    return submission


if __name__ == '__main__':
    raise SystemExit(0)
