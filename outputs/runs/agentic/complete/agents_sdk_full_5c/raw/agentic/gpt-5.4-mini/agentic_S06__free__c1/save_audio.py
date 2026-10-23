from __future__ import annotations

import os
from pathlib import Path
from typing import Union


def save_audio(audio_content: bytes, target: Union[str, Path]) -> str:
    path = Path(target)
    path.write_bytes(audio_content)
    return str(path)


if __name__ == "__main__":
    save_audio(b"", os.getenv("TTS_OUTPUT", "output.mp3"))
