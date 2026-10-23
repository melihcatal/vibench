import os
from typing import Union


def save_audio(audio_content: bytes, output_path: str, encoding: str = "MP3") -> str:
    if not output_path:
        raise ValueError("Output path must be provided")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as audio_file:
        audio_file.write(audio_content)

    return output_path
