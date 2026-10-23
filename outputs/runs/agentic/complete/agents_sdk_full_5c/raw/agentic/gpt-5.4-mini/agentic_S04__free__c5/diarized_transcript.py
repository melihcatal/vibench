from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from openai import OpenAI

from speech_client import SpeechServiceConfig, get_client
from speech_models import normalize_segments


def diarized_transcript(audio_file: str, *, language: Optional[str] = None) -> Dict[str, Any]:
    config = SpeechServiceConfig.from_env()
    client: OpenAI = get_client(config)
    with Path(audio_file).open("rb") as f:
        result: Dict[str, Any] = client.audio.transcriptions.create(
            model=config.transcribe_model,
            file=f,
            language=language,
            response_format="verbose_json",
            extra_body={"diarization": True},
        ).model_dump()
    segments = normalize_segments(result.get("segments", []))
    return {
        "text": result.get("text", ""),
        "segments": [segment.__dict__ for segment in segments],
        "provider": "openai",
        "model": config.transcribe_model,
    }
