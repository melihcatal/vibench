import os
import speech_client


def save_audio(audio_bytes: bytes, file_path: str) -> None:
    """Write synthesized speech audio to a local file.

    Args:
        audio_bytes (bytes): Audio data (e.g., MP3).
        file_path (str): Destination file path.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(audio_bytes)
