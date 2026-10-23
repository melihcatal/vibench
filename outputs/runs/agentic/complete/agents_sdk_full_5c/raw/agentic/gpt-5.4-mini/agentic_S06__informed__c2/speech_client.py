from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Iterable, List, Optional

import boto3
from botocore.client import BaseClient

from speech_models import VoiceOption, normalize_locale

AWS_REGION_ENV = "AWS_REGION"
AWS_DEFAULT_REGION_ENV = "AWS_DEFAULT_REGION"
AWS_ACCESS_KEY_ID_ENV = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV = "AWS_SECRET_ACCESS_KEY"


@dataclass
class SpeechClientConfig:
    provider: str = "amazon-polly"
    region: Optional[str] = None
    output_format: str = "mp3"
    sample_rate: str = "22050"


def load_config() -> SpeechClientConfig:
    region = os.getenv(AWS_REGION_ENV) or os.getenv(AWS_DEFAULT_REGION_ENV)
    return SpeechClientConfig(region=region)


def create_polly_client(config: Optional[SpeechClientConfig] = None) -> BaseClient:
    config = config or load_config()
    kwargs: dict[str, Any] = {}
    if config.region:
        kwargs["region_name"] = config.region
    return boto3.client("polly", **kwargs)


def list_voices(client: BaseClient, locale: Optional[str] = None) -> List[VoiceOption]:
    kwargs: dict[str, Any] = {}
    if locale:
        kwargs["LanguageCode"] = normalize_locale(locale) or locale
    result = client.describe_voices(**kwargs)
    voices = []
    for voice in result.get("Voices", []):
        voices.append(
            VoiceOption(
                name=voice.get("Id", ""),
                locale=voice.get("LanguageCode", ""),
                gender=voice.get("Gender"),
                style=voice.get("SupportedEngines", [None])[0],
                metadata=voice,
            )
        )
    return voices


def select_voice_for_locale(client: BaseClient, locale: str) -> Optional[VoiceOption]:
    voices = list_voices(client, locale=locale)
    return voices[0] if voices else None
