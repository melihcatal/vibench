import os
import io
from typing import Union, Optional, BinaryIO
from speech_models import TTSResponse


def save_audio_to_file(
    audio_response: TTSResponse, file_path: str, overwrite: bool = False
) -> str:
    if os.path.exists(file_path) and not overwrite:
        raise FileExistsError(f"File already exists: {file_path}")

    os.makedirs(
        os.path.dirname(os.path.abspath(file_path)), exist_ok=True
    ) if os.path.dirname(file_path) else None

    with open(file_path, "wb") as f:
        f.write(audio_response.audio_bytes)

    return file_path


def save_audio_to_stream(audio_response: TTSResponse, stream: BinaryIO) -> int:
    stream.write(audio_response.audio_bytes)
    return len(audio_response.audio_bytes)


def save_audio(
    audio_response: TTSResponse,
    destination: Union[str, BinaryIO],
    overwrite: bool = False,
) -> Union[str, int]:
    if isinstance(destination, str):
        return save_audio_to_file(audio_response, destination, overwrite=overwrite)
    elif hasattr(destination, "write"):
        return save_audio_to_stream(audio_response, destination)
    else:
        raise TypeError("destination must be a file path (str) or a writable stream")
