import io
from pathlib import Path
from typing import BinaryIO, Union

from openai import OpenAI


AudioDestination = Union[str, Path, BinaryIO, io.BytesIO]


def save_audio(audio: bytes, destination: AudioDestination) -> None:
    if hasattr(destination, "write"):
        destination.write(audio)
        if hasattr(destination, "flush"):
            destination.flush()
        return
    Path(destination).write_bytes(audio)


def synthesize_and_save(text: str, destination: AudioDestination, model: str = "gpt-4o-mini-tts", voice: str = "alloy") -> None:
    client = OpenAI()
    response = client.audio.speech.create(model=model, voice=voice, input=text, response_format="mp3")
    save_audio(response.read(), destination)
