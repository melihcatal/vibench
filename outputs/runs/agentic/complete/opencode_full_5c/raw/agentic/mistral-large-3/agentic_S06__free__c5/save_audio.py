import os
from typing import Union, IO


def save_audio(
    audio_content: bytes, output_path: str = None, file_obj: IO[bytes] = None
) -> Union[str, IO[bytes]]:
    """
    Writes synthesized speech audio to a local file or object.
    """
    if not output_path and not file_obj:
        raise ValueError("Either output_path or file_obj must be provided")

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(audio_content)
        return output_path

    if file_obj:
        file_obj.write(audio_content)
        return file_obj
