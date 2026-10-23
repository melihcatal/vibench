import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass(frozen=True)
class SpeechClientConfig:
    region_name: str
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    session_token: Optional[str] = None


def load_speech_client_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        session_token=os.getenv("AWS_SESSION_TOKEN"),
    )


def build_polly_client(config: Optional[SpeechClientConfig] = None):
    config = config or load_speech_client_config()
    kwargs: Dict[str, Any] = {"region_name": config.region_name}
    if config.access_key_id and config.secret_access_key:
        kwargs["aws_access_key_id"] = config.access_key_id
        kwargs["aws_secret_access_key"] = config.secret_access_key
    if config.session_token:
        kwargs["aws_session_token"] = config.session_token
    return boto3.client("polly", **kwargs)


def normalize_voice_name(voice_name: Optional[str]) -> Optional[str]:
    if not voice_name:
        return None
    return voice_name.strip()
