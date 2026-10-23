from typing import Union, IO
import os
from pathlib import Path


def save_audio(audio_bytes: bytes, output_path: Union[str, IO[bytes]]) -> None:
    """
    Write synthesized speech audio to a local file or object.
    """
    if isinstance(output_path, str):
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
    else:
        output_path.write(audio_bytes)