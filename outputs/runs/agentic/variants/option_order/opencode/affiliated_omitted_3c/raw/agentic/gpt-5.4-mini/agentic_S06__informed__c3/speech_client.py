import os
from dataclasses import dataclass
from typing import Optional

import boto3


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    return value if value else default


@dataclass(frozen=True)
class SpeechConfig:
    region_name: Optional[str] = None
    output_format: str = "mp3"
    voice_id: str = "Joanna"
    language_code: Optional[str] = None


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        region_name=_env("AWS_REGION", _env("AWS_DEFAULT_REGION")),
        output_format=_env("AWS_TTS_OUTPUT_FORMAT", "mp3"),
        voice_id=_env("AWS_TTS_VOICE_ID", "Joanna"),
        language_code=_env("AWS_TTS_LANGUAGE_CODE"),
    )


def create_polly_client(region_name: Optional[str] = None):
    cfg = load_speech_config()
    return boto3.client("polly", region_name=region_name or cfg.region_name)
