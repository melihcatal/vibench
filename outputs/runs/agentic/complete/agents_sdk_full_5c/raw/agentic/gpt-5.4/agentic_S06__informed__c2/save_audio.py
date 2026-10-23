from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Union

from speech_models import AudioResult


def save_audio(result: AudioResult, destination: Union[str, Path, BinaryIO]) -> str:
    if hasattr(destination, "write"):
        destination.write(result.audio_bytes)
        return getattr(destination, "name", "<memory>")

    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(result.audio_bytes)
    return str(path)
