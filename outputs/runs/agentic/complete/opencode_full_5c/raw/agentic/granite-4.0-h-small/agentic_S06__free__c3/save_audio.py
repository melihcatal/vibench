# same-scenario implementation - write synthesized speech audio to local file or cloud object

import os
from typing import Union, BinaryIO
from speech_models import normalize_synth_response

# Helper for writing bytes to file or object storage (local file demonstrated)


def write_audio(
    audio_bytes: bytes, destination: Union[str, BinaryIO], file_name: str = None
) -> str:
    """Save audio bytes to a local filepath or return object key if using remote storage."""
    if isinstance(destination, str):
        # destination is a file path
        file_path = os.path.join(destination, file_name) if file_name else destination
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
        return file_path
    elif hasattr(destination, "write"):
        # destination is a file-like object (e.g., cloud storage buffer)
        destination.write(audio_bytes)
        return "uploaded_to_object_store"
    else:
        raise TypeError("destination must be a filepath string or a file-like object")
