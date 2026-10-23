from pathlib import Path
from typing import Union

from speech_models import TextToSpeechResponse


def save_audio(speech: TextToSpeechResponse, destination: Union[str, Path]):
    path = Path(destination)
    path.write_bytes(speech.audio_bytes)
    return path
