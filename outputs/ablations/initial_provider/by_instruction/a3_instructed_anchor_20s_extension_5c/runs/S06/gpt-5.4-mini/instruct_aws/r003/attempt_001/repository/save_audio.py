from pathlib import Path


def save_audio(audio_bytes: bytes, destination: str) -> str:
    path = Path(destination)
    path.write_bytes(audio_bytes)
    return str(path)
