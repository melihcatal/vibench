from pathlib import Path
from typing import BinaryIO, Union


def save_audio(audio: bytes, target: Union[str, Path, BinaryIO]) -> None:
    if hasattr(target, "write"):
        target.write(audio)
        return
    Path(target).write_bytes(audio)
