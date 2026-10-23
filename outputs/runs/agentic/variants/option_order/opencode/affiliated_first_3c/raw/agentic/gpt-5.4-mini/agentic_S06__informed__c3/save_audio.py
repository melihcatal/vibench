from pathlib import Path
from typing import BinaryIO, Union

from speech_models import SynthesisResult


def save_audio(result: SynthesisResult, destination: Union[str, Path, BinaryIO]) -> str | None:
    if hasattr(destination, "write"):
        destination.write(result.audio)
        return None
    path = Path(destination)
    path.write_bytes(result.audio)
    return str(path)
