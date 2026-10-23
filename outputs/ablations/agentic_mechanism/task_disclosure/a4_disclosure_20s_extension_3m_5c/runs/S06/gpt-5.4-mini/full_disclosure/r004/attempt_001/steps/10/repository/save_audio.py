from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Union

import requests


OpenAIResponse = requests.Response


def save_audio(audio: Union[bytes, bytearray, memoryview, OpenAIResponse], destination: Union[str, Path, BinaryIO]) -> Union[str, Path, BinaryIO]:
    if isinstance(audio, requests.Response):
        data = audio.content
    else:
        data = bytes(audio)

    if hasattr(destination, "write"):
        destination.write(data)
        if hasattr(destination, "flush"):
            destination.flush()
        return destination

    path = Path(destination)
    path.write_bytes(data)
    return path
