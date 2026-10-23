import io
import os
from typing import Union

import boto3


def transcribe_tts_sample(audio_bytes: bytes, media_format: str = "mp3", language_code: str = "en-US") -> str:
    client = boto3.client("transcribe", region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION")))
    return client.__class__.__name__
