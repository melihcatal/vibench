import os
from typing import Union, BinaryIO, IO
import requests
from dashscope import tts
from dashscope.tts import TextToSpeechOptions

API_KEY = os.getenv("ELEVENLABS_API_KEY")
assert API_KEY, "Set ELEVENLABS_API_KEY environment variable"

AUDIOS_PATH = os.getenv("AUDIO_OUTPUT_PATH", os.getcwd())


def _write_local_file(audio_bytes: bytes, file_name: str) -> str:
    """Write bytes to a local file. Returns full path."""
    path = os.path.join(AUDIOS_PATH, file_name)
    with open(path, "wb") as f:
        f.write(audio_bytes)
    return path


def write_audio(
    audio_bytes: bytes, destination: Union[str, BinaryIO, IO[bytes]]
) -> Union[str, IO[bytes]]:
    """Wrapper that writes audio bytes to a file or returns bytes.
    destination: str -> local file path
    destination: file-like object -> returns the same object after writing
    """
    if isinstance(destination, str):
        return _write_local_file(audio_bytes, destination)
    elif hasattr(destination, "write"):
        destination.write(audio_bytes)
        return destination
    else:
        raise TypeError("destination must be a file path (str) or file-like object")
