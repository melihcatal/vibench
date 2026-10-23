from __future__ import annotations

from pathlib import Path
from typing import Union

from speech_models import SpeechResponse


def save_audio(audio: Union[bytes, SpeechResponse], path: str) -> str:
    payload = audio.audio if isinstance(audio, SpeechResponse) else audio
    target = Path(path)
    target.write_bytes(payload)
    return str(target)
