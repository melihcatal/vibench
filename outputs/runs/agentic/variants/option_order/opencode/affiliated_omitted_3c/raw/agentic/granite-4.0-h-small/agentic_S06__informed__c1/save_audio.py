import os
import wave
from typing import Union
from google.cloud import texttospeech


def save_audio(audio_bytes: bytes, file_path: str, fmt: str = "wav") -> None:
    """Save synthesized audio bytes to a local file.

    Args:
        audio_bytes (bytes): Audio data from TTS synthesis.
        file_path (str): Destination path (including extension).
        fmt (str): Output format ('wav' or 'mp3'; default 'wav').
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if fmt.lower() == "wav":
        with wave.open(file_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(audio_bytes)
    elif fmt.lower() == "mp3":
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
    else:
        raise ValueError(f"Unsupported format '{fmt}'. Use 'wav' or 'mp3'.")
