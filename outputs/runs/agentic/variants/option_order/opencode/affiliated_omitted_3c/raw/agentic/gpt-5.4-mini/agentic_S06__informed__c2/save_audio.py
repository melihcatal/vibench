from pathlib import Path
from typing import Union


def save_audio(
    audio: bytes, destination: Union[str, Path, object]
) -> Union[str, Path, object]:
    if hasattr(destination, "write"):
        destination.write(audio)
        return destination
    path = Path(destination)
    path.write_bytes(audio)
    return path
