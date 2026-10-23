# [SAME-SCENARIO] save_audio.py

import os
from pathlib import Path
from typing import Union
from .speech_client import TextToSpeechClient
from .speech_models import AudioConfig

def save_audio(
    audio_bytes: bytes,
    file_path: Union[str, Path],
    client: Optional[TextToSpeechClient] = None,
) -> Path:
    """Persist synthesized audio to a local file or cloud storage (placeholder for later extension).

    Args:
        audio_bytes: Raw audio bytes from provider synthesis response.
        file_path: Local filesystem path (or object storage key if client implements upload).
        client: Optional client for future cloud upload support.

    Returns:
        Path object representing the saved file.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(audio_bytes)
    return path
