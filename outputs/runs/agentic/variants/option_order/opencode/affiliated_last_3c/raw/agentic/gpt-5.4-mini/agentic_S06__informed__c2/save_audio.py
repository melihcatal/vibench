from pathlib import Path
from typing import Union

from speech_models import TTSResponse


def save_audio(audio: bytes, destination: Union[str, Path, object]) -> object:
    if hasattr(destination, "write"):
        destination.write(audio)
        return destination
    path = Path(destination)
    path.write_bytes(audio)
    return str(path)


def save_tts_response(
    response: TTSResponse, destination: Union[str, Path, object]
) -> object:
    return save_audio(response.audio, destination)
