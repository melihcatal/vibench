from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Union

from speech_models import SpeechSynthesisResult


def save_audio(
    target: Union[str, Path, BinaryIO], synthesis: SpeechSynthesisResult
) -> str:
    if hasattr(target, "write"):
        target.write(synthesis.audio_bytes)
        return getattr(target, "name", "<memory>")
    path = Path(target)
    path.write_bytes(synthesis.audio_bytes)
    return str(path)
