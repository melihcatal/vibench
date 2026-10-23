from pathlib import Path
from typing import Union

from speech_models import TTSResponse


def save_audio(audio: Union[TTSResponse, bytes], destination: Union[str, Path]) -> Path:
    data = audio.audio_bytes if isinstance(audio, TTSResponse) else audio
    path = Path(destination)
    path.write_bytes(data)
    return path
