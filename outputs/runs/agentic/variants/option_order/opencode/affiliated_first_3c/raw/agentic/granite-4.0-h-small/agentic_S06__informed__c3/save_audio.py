# [SAME-SCENARIO] save_audio.py
# Writes synthesized speech audio to a local file or returns raw bytes.

import os
from typing import Union, bytes
from pathlib import Path

# ---------- Configuration ----------
# No provider-specific keys needed for local file IO
# -----------------------------------


def save_audio(
    audio_bytes: bytes, target: Union[str, Path], file_name: str = "output.raw"
) -> Union[str, None]:
    """Save audio bytes to a local file or return the bytes.

    Args:
        audio_bytes (bytes): Raw audio data.
        target (Union[str, Path]): Destination path or directory.
        file_name (str): Name of the file when saving to a directory.

    Returns:
        Union[str, None]: Absolute file path if saved to disk, else None.
    """
    dest = Path(target) if isinstance(target, str) else target
    if dest.is_dir():
        dest /= file_name
    dest.write_bytes(audio_bytes)
    return str(dest.resolve())


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     # Assume audio_bytes is obtained from any TTS function
#     audio_bytes = b"\x00" * 1024
#     file_path = save_audio(audio_bytes, ".", "test.raw")
#     print("Audio saved to", file_path)
