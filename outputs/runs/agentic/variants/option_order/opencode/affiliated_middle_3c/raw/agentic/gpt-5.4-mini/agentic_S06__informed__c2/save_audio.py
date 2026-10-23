from pathlib import Path


def save_audio(audio: bytes, destination: str | Path | None = None) -> bytes | str:
    if destination is None:
        return audio
    path = Path(destination)
    path.write_bytes(audio)
    return str(path)
