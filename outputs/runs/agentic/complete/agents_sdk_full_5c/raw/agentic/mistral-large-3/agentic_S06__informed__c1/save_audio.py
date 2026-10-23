from typing import Union, IO
import os

def save_audio_to_file(
    audio_bytes: bytes,
    output_path: str,
    mode: str = "wb"
) -> None:
    """
    Write synthesized speech audio to a local file.
    """
    with open(output_path, mode) as audio_file:
        audio_file.write(audio_bytes)

def save_audio_to_object(
    audio_bytes: bytes,
    buffer: IO[bytes]
) -> None:
    """
    Write synthesized speech audio to a file-like object.
    """
    buffer.write(audio_bytes)