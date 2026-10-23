from pathlib import Path


def save_audio(audio_content: bytes, destination: str | Path) -> str:
    path = Path(destination)
    path.write_bytes(audio_content)
    return str(path)
