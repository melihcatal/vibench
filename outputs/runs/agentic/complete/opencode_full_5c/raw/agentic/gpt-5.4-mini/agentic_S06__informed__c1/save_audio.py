from pathlib import Path
from typing import Union


def save_audio(audio_content: bytes, destination: Union[str, Path, object]):
    if hasattr(destination, "write"):
        destination.write(audio_content)
        return destination
    path = Path(destination)
    path.write_bytes(audio_content)
    return str(path)
