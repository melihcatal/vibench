from pathlib import Path
from typing import BinaryIO, Union


def save_audio(audio: bytes, destination: Union[str, Path, BinaryIO]) -> str:
    if hasattr(destination, "write"):
        destination.write(audio)
        return getattr(destination, "name", "<stream>")
    path = Path(destination)
    path.write_bytes(audio)
    return str(path)
