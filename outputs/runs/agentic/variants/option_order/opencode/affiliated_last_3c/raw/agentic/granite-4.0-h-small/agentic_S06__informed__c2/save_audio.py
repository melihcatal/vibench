# [SAME-SCENARIO] save_audio.py
# Utility to write synthesized speech audio to a local file or object storage
import os
from pathlib import Path
from typing import Union


def write_audio(
    data: bytes, target_path: Union[str, Path], format: str = "mp3"
) -> Path:
    """Save raw audio bytes to a local file or S3-like object path.

    Args:
        data (bytes): Raw audio data (e.g., MP3 bytes).
        target_path (Union[str, Path]): Local file path or object storage key (e.g., 's3://bucket/key').
        format (str): Audio format indicator; currently only 'mp3' is supported.

    Returns:
        Path: Path object of the saved file (or None for object storage).
    """
    # Assume simple local file write for this demo
    if str(target_path).startswith("s3://"):
        # Placeholder for S3 upload logic - omitted for this example
        print(f"[INFO] Would upload audio to object storage at {target_path}")
        return None
    # Ensure directories exist
    Path(target_path).parent.mkdir(parents=True, exist_ok=True)
    full_path = Path(target_path)
    full_path.write_bytes(data)
    print(f"[INFO] Audio saved to {full_path}")
    return full_path
