from typing import Union, BinaryIO
import os


def save_audio(audio_content: bytes, output_path: Union[str, BinaryIO]) -> None:
    """
    Writes synthesized speech audio to a local file or object.

    Args:
        audio_content: The audio content as bytes.
        output_path: The file path or binary IO object to write the audio to.

    Raises:
        IOError: If the file cannot be written.
    """
    if isinstance(output_path, str):
        with open(output_path, "wb") as audio_file:
            audio_file.write(audio_content)
    else:
        output_path.write(audio_content)
