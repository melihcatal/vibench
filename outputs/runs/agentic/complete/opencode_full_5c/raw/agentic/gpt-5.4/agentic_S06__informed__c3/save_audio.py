from __future__ import annotations

from pathlib import Path
from typing import Union

from speech_models import SynthesisResult


def save_audio(result: SynthesisResult, destination: Union[str, Path]) -> Path:
    path = Path(destination)
    path.write_bytes(result.audio_bytes)
    return path
