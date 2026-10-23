from __future__ import annotations

from typing import BinaryIO, Union

from speech_models import AudioResult


def save_audio(audio: AudioResult, destination: Union[str, BinaryIO]) -> str:
    if hasattr(destination, "write"):
        destination.write(audio.audio_bytes)
        return getattr(destination, "name", "<memory>")
    with open(destination, "wb") as handle:
        handle.write(audio.audio_bytes)
    return destination
