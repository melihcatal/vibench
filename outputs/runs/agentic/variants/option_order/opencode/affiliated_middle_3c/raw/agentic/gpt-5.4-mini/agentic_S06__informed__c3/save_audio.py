from pathlib import Path
from typing import BinaryIO, Union


def save_audio(audio: bytes, destination: Union[str, Path, BinaryIO]):
    if hasattr(destination, "write"):
        destination.write(audio)
        return destination
    path = Path(destination)
    path.write_bytes(audio)
    return path
