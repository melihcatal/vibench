from pathlib import Path


def save_audio(audio_bytes: bytes, target: str | Path | None = None):
    if target is None:
        return audio_bytes
    path = Path(target)
    path.write_bytes(audio_bytes)
    return str(path)
