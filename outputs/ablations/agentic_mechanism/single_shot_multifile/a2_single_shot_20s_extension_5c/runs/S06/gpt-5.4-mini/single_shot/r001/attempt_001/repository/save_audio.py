from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from speech_client import build_tts_client
from speech_models import TextToSpeechRequest, normalize_text_request


def save_audio(text: str, output_path: str | Path | BinaryIO, voice: str | None = None, locale: str | None = None) -> str | None:
    client = build_tts_client()
    request = normalize_text_request(TextToSpeechRequest(text=text, voice=voice, locale=locale))
    response = client.synthesize_text(request)
    if hasattr(output_path, 'write'):
        output_path.write(response.audio)
        return None
    path = Path(output_path)
    path.write_bytes(response.audio)
    return str(path)
