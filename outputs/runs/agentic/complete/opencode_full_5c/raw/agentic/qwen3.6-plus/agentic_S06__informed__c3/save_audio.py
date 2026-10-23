import os
from typing import Union


def save_audio(
    audio_bytes: bytes, output_path: str, content_type: str = "audio/mpeg"
) -> str:
    if not output_path:
        ext = _ext_from_content_type(content_type)
        output_path = f"output{ext}"
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    return output_path


def _ext_from_content_type(content_type: str) -> str:
    mapping = {
        "audio/mpeg": ".mp3",
        "audio/wav": ".wav",
        "audio/ogg": ".ogg",
        "audio/flac": ".flac",
        "audio/aac": ".aac",
        "audio/mulaw": ".mulaw",
    }
    return mapping.get(content_type, ".mp3")
