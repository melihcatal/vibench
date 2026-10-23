from pathlib import Path

from speech_models import TextToSpeechResponse


def save_audio(response: TextToSpeechResponse, destination: str):
    path = Path(destination)
    path.write_bytes(response.audio_bytes)
    return str(path)
