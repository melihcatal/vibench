import os
from pathlib import Path
from typing import BinaryIO, Optional, Union

from openai import OpenAI


def save_audio(audio: bytes, target: Union[str, os.PathLike, BinaryIO]) -> Optional[str]:
    if hasattr(target, "write"):
        target.write(audio)
        return None
    path = Path(target)
    path.write_bytes(audio)
    return str(path)


def synthesize_and_save(text: str, target: Union[str, os.PathLike, BinaryIO], voice: str = "alloy", model: str = "gpt-4o-mini-tts") -> Optional[str]:
    client = OpenAI()
    response = client.audio.speech.create(model=model, voice=voice, input=text)
    audio = response.read()
    return save_audio(audio, target)
