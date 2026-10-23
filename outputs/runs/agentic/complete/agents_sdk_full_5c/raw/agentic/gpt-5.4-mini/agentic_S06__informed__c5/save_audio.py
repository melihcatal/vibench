from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Union

from speech_models import TextToSpeechResponse


Target = Union[str, Path, BinaryIO]


def save_audio(response: TextToSpeechResponse, target: Target) -> int:
    data = response.audio_bytes
    if hasattr(target, "write"):
        return target.write(data)
    path = Path(target)
    path.write_bytes(data)
    return len(data)
