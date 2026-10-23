from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Union

from speech_models import SynthesisResult


def save_audio(target: Union[str, Path, BinaryIO], result: SynthesisResult) -> str | None:
    if hasattr(target, "write"):
        target.write(result.audio_bytes)
        return None
    path = Path(target)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(result.audio_bytes)
    return str(path)
