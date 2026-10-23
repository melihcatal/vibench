import os
from pathlib import Path
from speech_models import TTSResponse


def save_audio_to_file(response: TTSResponse, output_path: str) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(response.audio_bytes)
    return str(path)


def save_audio_bytes(
    audio_bytes: bytes, output_path: str, content_type: str = "audio/mpeg"
) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(audio_bytes)
    return str(path)


def save_audio_with_extension(
    response: TTSResponse, directory: str, filename: str
) -> str:
    ext_map = {
        "audio/mpeg": ".mp3",
        "audio/wav": ".wav",
        "audio/ogg": ".ogg",
        "audio/flac": ".flac",
    }
    ext = ext_map.get(response.content_type, ".mp3")
    output_path = os.path.join(directory, f"{filename}{ext}")
    return save_audio_to_file(response, output_path)
