from pathlib import Path
from typing import Union


def save_audio(audio: bytes, destination: Union[str, Path, None] = None):
    if destination is None:
        return audio
    path = Path(destination)
    path.write_bytes(audio)
    return str(path)
