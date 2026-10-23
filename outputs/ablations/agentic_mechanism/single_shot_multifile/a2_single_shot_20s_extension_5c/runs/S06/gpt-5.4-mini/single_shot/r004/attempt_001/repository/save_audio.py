from __future__ import annotations

from pathlib import Path
from typing import Union


def save_audio(audio: bytes, destination: Union[str, Path]) -> str:
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(audio)
    return str(path)
