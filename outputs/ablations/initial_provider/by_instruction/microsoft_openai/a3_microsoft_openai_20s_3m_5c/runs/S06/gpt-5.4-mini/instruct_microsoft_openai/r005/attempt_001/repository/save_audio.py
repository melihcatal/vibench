from pathlib import Path

from speech_models import extract_audio_bytes


def save_audio(audio, path):
    data = extract_audio_bytes(audio)
    if hasattr(path, "write"):
        path.write(data)
        return path
    Path(path).write_bytes(data)
    return path
