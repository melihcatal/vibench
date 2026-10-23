import os
from speech_models import TTSResponse


def save_audio_to_file(response: TTSResponse, output_path: str) -> str:
    audio_bytes = response.audio_bytes
    os.makedirs(
        os.path.dirname(os.path.abspath(output_path)), exist_ok=True
    ) if os.path.dirname(output_path) else None
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    return output_path


def save_audio_bytes_to_file(
    audio_bytes: bytes, output_path: str, content_type: str = "audio/mpeg"
) -> str:
    os.makedirs(
        os.path.dirname(os.path.abspath(output_path)), exist_ok=True
    ) if os.path.dirname(output_path) else None
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    return output_path
