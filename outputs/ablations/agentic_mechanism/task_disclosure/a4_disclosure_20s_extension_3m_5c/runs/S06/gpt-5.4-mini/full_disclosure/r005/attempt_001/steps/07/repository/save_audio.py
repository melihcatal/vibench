import os
from pathlib import Path
from typing import BinaryIO, Union

OPENAI_TTS_API_URL = "https://api.openai.com/v1/audio/speech"


def save_audio(audio: bytes, destination: Union[str, os.PathLike, BinaryIO]) -> Union[str, BinaryIO]:
    if not isinstance(audio, (bytes, bytearray)) or not audio:
        raise ValueError("audio must be non-empty bytes")

    if hasattr(destination, "write"):
        destination.write(audio)
        if hasattr(destination, "flush"):
            destination.flush()
        return destination

    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(bytes(audio))
    return str(path)
