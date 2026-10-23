import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    return value if value not in ('', None) else default


@dataclass
class SpeechConfig:
    region_name: str
    output_bucket: Optional[str] = None
    media_format: Optional[str] = None
    language_code: str = 'en-US'
    vocabulary_name: Optional[str] = None
    terminology_name: Optional[str] = None
    model_settings: Optional[Dict[str, Any]] = None


def load_config() -> SpeechConfig:
    return SpeechConfig(
        region_name=_env('AWS_REGION', _env('AWS_DEFAULT_REGION', 'us-east-1')),
        output_bucket=_env('AWS_TRANSCRIBE_OUTPUT_BUCKET'),
        media_format=_env('AWS_TRANSCRIBE_MEDIA_FORMAT'),
        language_code=_env('AWS_TRANSCRIBE_LANGUAGE_CODE', 'en-US'),
        vocabulary_name=_env('AWS_TRANSCRIBE_VOCABULARY_NAME'),
        terminology_name=_env('AWS_TRANSCRIBE_TERMINOLOGY_NAME'),
    )


def transcribe_client(region_name: Optional[str] = None):
    config = load_config()
    return boto3.client('transcribe', region_name=region_name or config.region_name)


def s3_client(region_name: Optional[str] = None):
    config = load_config()
    return boto3.client('s3', region_name=region_name or config.region_name)


def normalize_s3_uri(value: str) -> str:
    if value.startswith('s3://'):
        return value
    bucket, _, key = value.partition('/')
    return f's3://{bucket}/{key}' if key else f's3://{bucket}'
