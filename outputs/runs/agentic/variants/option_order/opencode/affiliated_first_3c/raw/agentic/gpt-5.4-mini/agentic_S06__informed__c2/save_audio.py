from pathlib import Path

from speech_models import SpeechResponse


def save_audio(response: SpeechResponse, target):
    data = response.audio
    if hasattr(target, "write"):
        target.write(data)
        return target
    path = Path(target)
    path.write_bytes(data)
    return str(path)
