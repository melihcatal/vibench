import os
from typing import Union, BinaryIO
from speech_models import SynthesisResponse


def save_audio(
    audio_stream: BinaryIO,
    output_path: Union[str, os.PathLike],
    format: str = "wav"
) -> None:
    if isinstance(output_path, str):
        output_path = os.path.expanduser(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as f:
        for chunk in audio_stream:
            if isinstance(chunk, SynthesisResponse):
                f.write(chunk.audio_chunk)
            else:
                f.write(chunk)