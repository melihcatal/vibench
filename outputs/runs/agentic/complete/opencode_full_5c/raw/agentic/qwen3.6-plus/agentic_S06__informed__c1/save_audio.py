import os
from pathlib import Path
from speech_models import TTSResponse


def save_audio(
    response: TTSResponse,
    output_path: str,
    overwrite: bool = False,
) -> str:
    path = Path(output_path)
    if path.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {output_path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(response.audio_bytes)
    return str(path.resolve())


def save_audio_bytes(
    audio_bytes: bytes,
    output_path: str,
    content_type: str = "audio/mpeg",
    overwrite: bool = False,
) -> str:
    path = Path(output_path)
    if path.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {output_path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(audio_bytes)
    return str(path.resolve())
