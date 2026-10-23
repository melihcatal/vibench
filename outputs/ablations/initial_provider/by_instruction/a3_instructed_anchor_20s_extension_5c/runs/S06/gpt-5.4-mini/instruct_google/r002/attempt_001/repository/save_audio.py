from pathlib import Path


def save_audio(audio_content: bytes, path: str) -> str:
    target = Path(path)
    target.write_bytes(audio_content)
    return str(target)
