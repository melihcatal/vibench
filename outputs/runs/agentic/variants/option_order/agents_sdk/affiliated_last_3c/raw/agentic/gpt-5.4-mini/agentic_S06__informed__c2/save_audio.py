from __future__ import annotations

from pathlib import Path
from typing import BinaryIO


def save_audio(audio_bytes: bytes, destination: str | Path | BinaryIO) -> str | Path | BinaryIO:
    if hasattr(destination, "write"):
        destination.write(audio_bytes)
        return destination
    path = Path(destination)
    path.write_bytes(audio_bytes)
    return path
