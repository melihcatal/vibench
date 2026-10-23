from typing import Union
import os


def save_audio(
    audio_content: bytes, output_path: str, content_type: str = "audio/mpeg"
) -> None:
    """
    Writes synthesized speech audio to a local file or object.
    """
    with open(output_path, "wb") as audio_file:
        audio_file.write(audio_content)
