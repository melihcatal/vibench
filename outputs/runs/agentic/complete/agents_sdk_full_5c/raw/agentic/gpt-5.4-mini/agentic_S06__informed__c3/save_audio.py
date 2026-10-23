from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Union

from speech_client import synthesize_with_azure
from speech_models import TextToSpeechRequest


def save_audio(target: Union[str, Path, BinaryIO], text: str, voice: str | None = None, locale: str | None = None) -> int:
    audio = synthesize_with_azure(TextToSpeechRequest(text=text, voice=voice, locale=locale)).audio_bytes
    if hasattr(target, "write"):
        return target.write(audio)
    path = Path(target)
    path.write_bytes(audio)
    return len(audio)
