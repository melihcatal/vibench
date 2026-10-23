import os
from pathlib import Path
from speech_client import get_openai_client
from speech_models import AudioOutput


def save_audio(
    audio_bytes: bytes,
    output_path: str | Path,
    content_type: str = "audio/mpeg",
) -> AudioOutput:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(audio_bytes)
    return AudioOutput(
        file_path=str(path),
        size_bytes=len(audio_bytes),
        content_type=content_type,
        provider="openai",
    )
