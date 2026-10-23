from pathlib import Path


def save_audio(audio: bytes, destination: str) -> str:
    path = Path(destination)
    path.write_bytes(audio)
    return str(path)
