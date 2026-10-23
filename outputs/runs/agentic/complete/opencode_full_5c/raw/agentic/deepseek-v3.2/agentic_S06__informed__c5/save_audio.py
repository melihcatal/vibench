import os
from typing import Union
import wave
import io


def save_audio_to_file(audio_bytes: bytes, filepath: str, format: str = "mp3") -> str:
    """
    Write synthesized speech audio to a local file.
    """
    try:
        if format.lower() == "wav":
            with wave.open(filepath, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(24000)
                wav_file.writeframes(audio_bytes)
        else:
            with open(filepath, "wb") as f:
                f.write(audio_bytes)

        return filepath

    except Exception as e:
        raise Exception(f"Failed to save audio to file: {str(e)}")


def save_audio_to_bytesio(audio_bytes: bytes, format: str = "mp3") -> io.BytesIO:
    """
    Write synthesized speech audio to a BytesIO object.
    """
    try:
        audio_stream = io.BytesIO(audio_bytes)
        audio_stream.seek(0)
        return audio_stream

    except Exception as e:
        raise Exception(f"Failed to create audio stream: {str(e)}")
