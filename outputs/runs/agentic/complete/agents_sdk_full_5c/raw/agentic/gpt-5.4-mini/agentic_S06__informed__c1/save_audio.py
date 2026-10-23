from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Union

from speech_models import SpeechResponse


PathLike = Union[str, Path]


def save_audio(response: SpeechResponse, destination: Union[PathLike, BinaryIO]) -> str:
    if hasattr(destination, "write"):
        destination.write(response.audio_content)
        return getattr(destination, "name", "<memory>")
    path = Path(destination)
    path.write_bytes(response.audio_content)
    return str(path)
