from pathlib import Path


def save_audio(audio: bytes, target):
    if hasattr(target, "write"):
        target.write(audio)
        return target
    path = Path(target)
    path.write_bytes(audio)
    return str(path)
