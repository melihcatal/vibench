from __future__ import annotations

from pathlib import Path

from speech_models import AudioArtifact


def save_audio(artifact: AudioArtifact, destination: str) -> str:
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(artifact.audio_bytes)
    return str(path)
