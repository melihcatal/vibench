from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from speech_models import TTSResponse


def save_audio(response: TTSResponse, destination: str | Path | BinaryIO) -> str | None:
    data = response.audio_bytes
    if hasattr(destination, "write"):
        destination.write(data)
        return None
    path = Path(destination)
    path.write_bytes(data)
    return str(path)
