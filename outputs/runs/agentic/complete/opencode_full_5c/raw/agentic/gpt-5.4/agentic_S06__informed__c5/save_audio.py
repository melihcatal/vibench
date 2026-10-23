from __future__ import annotations

from pathlib import Path

from speech_models import AudioResult


def save_audio(audio: AudioResult, destination: str | Path | object) -> str | object:
    if hasattr(destination, "write"):
        destination.write(audio.audio_bytes)
        if hasattr(destination, "flush"):
            destination.flush()
        return destination
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(audio.audio_bytes)
    return str(path)
