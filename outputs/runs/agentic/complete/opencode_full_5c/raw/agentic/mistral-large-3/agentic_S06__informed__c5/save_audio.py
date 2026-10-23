from typing import Union, IO
import os


class AudioSaver:
    """Writes synthesized speech audio to a local file or object."""

    @staticmethod
    def save(audio_bytes: bytes, destination: Union[str, IO[bytes]]) -> None:
        """Save audio bytes to a file or file-like object."""
        if isinstance(destination, str):
            with open(destination, "wb") as f:
                f.write(audio_bytes)
        else:
            destination.write(audio_bytes)
