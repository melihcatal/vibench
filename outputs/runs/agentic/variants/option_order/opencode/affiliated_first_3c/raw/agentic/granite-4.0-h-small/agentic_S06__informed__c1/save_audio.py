import os
import shutil
import pathlib
from speech_client import TextToSpeechClient


def save_audio(audio_bytes: bytes, output_path: str, format_hint: str = None) -> str:
    """Write synthesized audio bytes to a local file or default object storage path.

    Args:
        audio_bytes (bytes): Audio content to persist.
        output_path (str): Destination file path (e.g., /tmp/output.wav) or a target object-store base directory.
        format_hint (str, optional): Hint to force a file extension (e.g., 'wav', 'mp3').

    Returns:
        str: The absolute path where the file was written.
    """
    abs_path = os.path.abspath(output_path)
    dir_path = os.path.dirname(abs_path)
    os.makedirs(dir_path, exist_ok=True)
    # Append extension if a hint is given and the path lacks one
    if format_hint and not pathlib.Path(abs_path).suffix:
        abs_path = f"{abs_path}.{format_hint}"
    with open(abs_path, "wb") as f:
        f.write(audio_bytes)
    return abs_path
