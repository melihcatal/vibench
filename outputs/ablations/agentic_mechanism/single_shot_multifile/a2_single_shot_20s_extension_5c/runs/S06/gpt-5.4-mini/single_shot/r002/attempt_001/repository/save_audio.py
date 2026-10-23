from pathlib import Path
from typing import Union


def save_audio(audio: bytes, target: Union[str, Path]) -> str:
    path = Path(target)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(audio)
    return str(path)
