from __future__ import annotations

from pathlib import Path
from typing import Union


def save_audio(audio: bytes, destination: Union[str, Path, object]) -> None:
    if hasattr(destination, "write"):
        destination.write(audio)
        return
    path = Path(destination)
    path.write_bytes(audio)
