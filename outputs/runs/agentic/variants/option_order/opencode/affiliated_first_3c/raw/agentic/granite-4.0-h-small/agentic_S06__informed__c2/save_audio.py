# [SAME-SCENARIO] save_audio.py
# Writes synthesized speech audio to a local file or object storage

import os
from pathlib import Path

# Helper import for storage adapters (example placeholder)
from speech_client import get_storage_adapter


def save_audio(audio_bytes: bytes, target: str, storage: str = "local") -> str:
    """Save audio bytes to a destination.

    Args:
        audio_bytes (bytes): Raw audio data.
        target (str): Destination path (file path or remote key).
        storage (str): 'local' or a cloud storage identifier (e.g., 's3', 'gs').

    Returns:
        str: Path or identifier where audio was stored.
    """
    if storage == "local":
        # Ensure directory exists
        dir_path = Path(target).parent
        dir_path.mkdir(parents=True, exist_ok=True)
        full_path = Path(target)
        full_path.write_bytes(audio_bytes)
        return str(full_path)
    else:
        # Delegate to configured storage adapter (e.g., S3, GCS)
        return get_storage_adapter(storage).upload(audio_bytes, target)
