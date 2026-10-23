from pathlib import Path
from typing import Union, BinaryIO

from speech_models import SpeechResponse


def save_audio(
    response: SpeechResponse, destination: Union[str, Path, BinaryIO]
) -> Union[str, Path]:
    if hasattr(destination, "write"):
        destination.write(response.audio)
        return destination
    path = Path(destination)
    path.write_bytes(response.audio)
    return path
