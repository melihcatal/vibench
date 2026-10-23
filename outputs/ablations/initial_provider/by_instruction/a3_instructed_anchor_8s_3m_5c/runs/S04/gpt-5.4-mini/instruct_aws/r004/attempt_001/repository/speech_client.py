import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class SpeechConfig:
    region: str
    bucket: Optional[str]
    prefix: str
    language_code: str
    vocabulary_name: Optional[str]
    transcribe: object


def load_config() -> SpeechConfig:
    import boto3

    session = boto3.Session()
    region = os.getenv("AWS_REGION") or session.region_name or "us-east-1"
    return SpeechConfig(
        region=region,
        bucket=os.getenv("SPEECH_STT_BUCKET"),
        prefix=os.getenv("SPEECH_STT_PREFIX", "transcriptions/"),
        language_code=os.getenv("SPEECH_LANGUAGE_CODE", "en-US"),
        vocabulary_name=os.getenv("SPEECH_VOCABULARY_NAME"),
        transcribe=session.client("transcribe", region_name=region),
    )


def s3_uri(bucket: str, key: str) -> str:
    return f"s3://{bucket}/{key.lstrip('/')}"


def normalize_job_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in value).strip("-")[:200]
