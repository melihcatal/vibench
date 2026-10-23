from pathlib import Path

from speech_models import SpeechResponse


def save_audio(audio: SpeechResponse, path: str) -> str:
    target = Path(path)
    target.write_bytes(audio.audio_bytes)
    return str(target)


def save_audio_bytes(audio_bytes: bytes, path: str) -> str:
    target = Path(path)
    target.write_bytes(audio_bytes)
    return str(target)
