from pathlib import Path


def save_audio(audio_bytes, destination):
    if hasattr(destination, "write"):
        destination.write(audio_bytes)
        return destination
    path = Path(destination)
    path.write_bytes(audio_bytes)
    return str(path)
