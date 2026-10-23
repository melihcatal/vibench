import os
from functools import lru_cache

import boto3


def aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


@lru_cache(maxsize=1)
def polly_client():
    return boto3.client("polly", region_name=aws_region())


def tts_voice(locale: str | None = None) -> str:
    mapping = {
        "en-US": os.getenv("AWS_POLLY_VOICE_EN_US", "Joanna"),
        "en-GB": os.getenv("AWS_POLLY_VOICE_EN_GB", "Amy"),
        "es-ES": os.getenv("AWS_POLLY_VOICE_ES_ES", "Lucia"),
        "fr-FR": os.getenv("AWS_POLLY_VOICE_FR_FR", "Celine"),
    }
    return mapping.get(locale or "", os.getenv("AWS_POLLY_DEFAULT_VOICE", "Joanna"))


def supported_voices():
    client = polly_client()
    resp = client.describe_voices()
    return resp.get("Voices", [])
