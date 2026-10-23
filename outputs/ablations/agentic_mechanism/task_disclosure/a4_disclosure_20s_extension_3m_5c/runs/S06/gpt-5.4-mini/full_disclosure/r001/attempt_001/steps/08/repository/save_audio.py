from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Union

import boto3


def save_audio(audio: bytes, destination: Union[str, Path, BinaryIO]) -> str:
    if isinstance(destination, (str, Path)):
        path = Path(destination)
        path.write_bytes(audio)
        return str(path)
    destination.write(audio)
    return getattr(destination, "name", "")


def save_speech_from_s3(bucket: str, key: str, destination: Union[str, Path, BinaryIO]) -> str:
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=bucket, Key=key)
    audio = obj["Body"].read()
    return save_audio(audio, destination)
