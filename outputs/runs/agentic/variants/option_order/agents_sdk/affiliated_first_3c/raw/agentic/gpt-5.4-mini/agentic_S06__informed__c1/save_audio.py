from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Union

from speech_client import synthesize_text_request
from speech_models import TTSRequest


Destination = Union[str, Path, BinaryIO]


def save_audio(text: str, destination: Destination, voice_name: str | None = None) -> Path | None:
    response = synthesize_text_request(TTSRequest(text=text, voice_name=voice_name))
    if hasattr(destination, "write"):
        destination.write(response.audio)
        return None
    path = Path(destination)
    path.write_bytes(response.audio)
    return path
