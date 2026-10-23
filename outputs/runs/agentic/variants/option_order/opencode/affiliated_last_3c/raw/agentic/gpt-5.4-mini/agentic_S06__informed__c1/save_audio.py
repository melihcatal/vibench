from pathlib import Path
from typing import BinaryIO, Union


def save_audio(
    audio: bytes, target: Union[str, Path, BinaryIO]
) -> Union[str, Path, BinaryIO]:
    if hasattr(target, "write"):
        target.write(audio)
        return target
    path = Path(target)
    path.write_bytes(audio)
    return path
