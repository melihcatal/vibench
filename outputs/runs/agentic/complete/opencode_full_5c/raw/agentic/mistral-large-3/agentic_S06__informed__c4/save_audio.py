from typing import Union, BinaryIO
import io
import wave


def save_audio(
    audio_bytes: bytes, output_path: Union[str, BinaryIO], format: str = "wav"
) -> None:
    """Write synthesized speech audio to a local file or object."""
    if isinstance(output_path, str):
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
    else:
        output_path.write(audio_bytes)
