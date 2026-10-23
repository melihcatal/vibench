import os
from typing import Union
from speech_models import TTSResponse


def save_audio(response: TTSResponse, output_path: str, overwrite: bool = False) -> str:
    if os.path.exists(output_path) and not overwrite:
        raise FileExistsError(f"Output file already exists: {output_path}")

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(response.audio_content)

    return output_path


def save_audio_bytes(
    audio_bytes: bytes,
    output_path: str,
    audio_format: str = "MP3",
    overwrite: bool = False,
) -> str:
    if os.path.exists(output_path) and not overwrite:
        raise FileExistsError(f"Output file already exists: {output_path}")

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    return output_path


def get_audio_extension(audio_format: str) -> str:
    extension_map = {
        "MP3": ".mp3",
        "LINEAR16": ".wav",
        "OGG_OPUS": ".ogg",
        "MULAW": ".au",
        "ALAW": ".wav",
    }
    return extension_map.get(audio_format.upper(), ".mp3")


def build_output_path(base_name: str, audio_format: str, output_dir: str = ".") -> str:
    ext = get_audio_extension(audio_format)
    return os.path.join(output_dir, f"{base_name}{ext}")
