from pathlib import Path

from speech_models import TextToSpeechResult


def save_audio(result: TextToSpeechResult, destination: str) -> str:
    path = Path(destination)
    path.write_bytes(result.audio_bytes)
    return str(path)
