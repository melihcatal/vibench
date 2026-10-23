from pathlib import Path


def save_audio(audio: bytes, path: str = None):
    if path:
        target = Path(path)
        target.write_bytes(audio)
        return str(target)
    return audio
