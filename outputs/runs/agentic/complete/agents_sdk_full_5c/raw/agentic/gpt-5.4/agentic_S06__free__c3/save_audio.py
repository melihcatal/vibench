from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Union

from speech_models import AudioResult


WritableTarget = Union[str, Path, BinaryIO]


def save_audio(result: AudioResult, target: WritableTarget) -> str:
    if hasattr(target, "write"):
        target.write(result.audio_bytes)
        return getattr(target, "name", "<memory>")
    path = Path(target)
    path.write_bytes(result.audio_bytes)
    return str(path)
