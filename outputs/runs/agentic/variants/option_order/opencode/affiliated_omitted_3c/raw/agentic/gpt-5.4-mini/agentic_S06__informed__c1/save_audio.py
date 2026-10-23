from pathlib import Path
from typing import Union


def save_audio(audio_content: bytes, destination: Union[str, Path]) -> str:
    path = Path(destination)
    path.write_bytes(audio_content)
    return str(path)
