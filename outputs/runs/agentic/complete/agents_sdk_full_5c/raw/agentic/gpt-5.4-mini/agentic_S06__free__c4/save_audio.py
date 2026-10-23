from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Union

from synthesize_text import synthesize_text


Destination = Union[str, Path, BinaryIO]


def save_audio(text: str, destination: Destination) -> bytes:
    audio = synthesize_text(text)
    if hasattr(destination, "write"):
        destination.write(audio)
    else:
        Path(destination).write_bytes(audio)
    return audio
