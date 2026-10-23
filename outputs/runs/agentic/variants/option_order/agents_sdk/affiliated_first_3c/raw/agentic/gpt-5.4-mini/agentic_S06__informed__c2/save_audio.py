from __future__ import annotations

from pathlib import Path
from typing import Union

from speech_models import TTSResponse


def save_audio(response: TTSResponse, destination: Union[str, Path]) -> Path:
    path = Path(destination)
    path.write_bytes(response.audio)
    return path
