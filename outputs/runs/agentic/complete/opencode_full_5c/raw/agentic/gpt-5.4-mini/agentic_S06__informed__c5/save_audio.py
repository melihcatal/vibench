from typing import BinaryIO, Union


def save_audio(audio: bytes, destination: Union[str, BinaryIO]):
    if isinstance(destination, str):
        with open(destination, "wb") as f:
            f.write(audio)
        return destination
    destination.write(audio)
    return destination
