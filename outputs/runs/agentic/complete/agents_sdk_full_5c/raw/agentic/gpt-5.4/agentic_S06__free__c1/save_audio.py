from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Union

from speech_models import TTSResponse


def save_audio(target: Union[str, Path, BinaryIO], response: TTSResponse) -> str:
    if hasattr(target, "write"):
        target.write(response.audio_bytes)
        return getattr(target, "name", "<memory-stream>")

    path = Path(target)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(response.audio_bytes)
    return str(path)
