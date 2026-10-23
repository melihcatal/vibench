from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import get_client, load_config
from speech_models import build_timestamped_payload, normalize_timestamped_output


def timestamped_transcript(audio_path: str, *, words: bool = True, language: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    config = load_config()
    client = get_client(config)
    payload = build_timestamped_payload(audio_path=audio_path, words=words, language=language or config.default_language, model=model or config.default_model)
    result = client.transcriptions.create(payload)
    return normalize_timestamped_output(result)
