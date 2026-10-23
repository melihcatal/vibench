import os
from dataclasses import asdict
from typing import Any, Dict, Optional

from assemblyai import Transcriber

from speech_models import (
    TranscriptionRequest,
    TranscriptionResult,
    normalize_segments,
    normalize_text,
)


def get_api_key() -> Optional[str]:
    return os.getenv("ASSEMBLYAI_API_KEY")


def build_transcriber() -> Transcriber:
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")
    return Transcriber(api_key)


def request_to_kwargs(request: TranscriptionRequest) -> Dict[str, Any]:
    payload = asdict(request)
    return {key: value for key, value in payload.items() if value is not None}


def response_to_result(item: Any) -> TranscriptionResult:
    data = item if isinstance(item, dict) else getattr(item, "__dict__", {})
    text = normalize_text(data)
    segments = normalize_segments(data)
    words = normalize_segments(data.get("words") if isinstance(data, dict) else None)
    return TranscriptionResult(
        id=str(data.get("id", "")),
        status=str(data.get("status", "")),
        text=text,
        segments=segments,
        words=words,
        error=data.get("error"),
    )
