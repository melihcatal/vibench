from pathlib import Path

from speech_models import SpeechResponse


def save_audio(response: SpeechResponse, destination: str) -> str:
    path = Path(destination)
    path.write_bytes(response.audio)
    return str(path)
