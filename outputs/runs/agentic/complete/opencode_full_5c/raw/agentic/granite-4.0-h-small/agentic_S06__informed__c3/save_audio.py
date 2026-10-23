import os
import pathlib
from typing import Union


def write_audio_file(data: bytes, path: Union[str, pathlib.Path]) -> pathlib.Path:
    """Write raw audio bytes (PCM) to a local file.

    Args:
        data (bytes): Binary audio content.
        path (str|Path): Destination file path (e.g., "output.wav").

    Returns:
        pathlib.Path: Resolved absolute path of the saved file.
    """
    resolved = pathlib.Path(path).resolve()
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_bytes(data)
    return resolved


# Minimal example of using helper to save Azure TTS result
# audio = synthesize_text("Hello world", output_file="hello.wav")
