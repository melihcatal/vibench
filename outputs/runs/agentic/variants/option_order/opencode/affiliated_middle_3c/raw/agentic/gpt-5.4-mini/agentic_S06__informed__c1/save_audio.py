from pathlib import Path
from typing import Union


def save_audio(audio_bytes: bytes, destination: Union[str, Path, object]):
    if hasattr(destination, "write"):
        destination.write(audio_bytes)
        return destination
    path = Path(destination)
    path.write_bytes(audio_bytes)
    return str(path)
