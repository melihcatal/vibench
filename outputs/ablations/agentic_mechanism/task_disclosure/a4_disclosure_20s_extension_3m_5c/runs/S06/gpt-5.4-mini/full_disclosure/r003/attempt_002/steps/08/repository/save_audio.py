import os
from pathlib import Path
from typing import BinaryIO, Optional, Union

from synthesize_text import synthesize_text


def save_audio(audio: bytes, destination: Union[str, os.PathLike, BinaryIO], overwrite: bool = True) -> Optional[str]:
    if audio is None:
        raise ValueError("audio must not be None")
    if isinstance(destination, (str, os.PathLike)):
        path = Path(destination)
        if path.exists() and not overwrite:
            raise FileExistsError(str(path))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(audio)
        return str(path)
    if hasattr(destination, "write"):
        destination.write(audio)
        return None
    raise TypeError("destination must be a path or writable binary file-like object")


def synthesize_and_save(text: str, destination: Union[str, os.PathLike, BinaryIO], voice: str = "alloy", format: str = "mp3", speed: float = 1.0, api_key: Optional[str] = None, overwrite: bool = True) -> Optional[str]:
    audio = synthesize_text(text=text, voice=voice, format=format, speed=speed, api_key=api_key)
    return save_audio(audio, destination, overwrite=overwrite)
