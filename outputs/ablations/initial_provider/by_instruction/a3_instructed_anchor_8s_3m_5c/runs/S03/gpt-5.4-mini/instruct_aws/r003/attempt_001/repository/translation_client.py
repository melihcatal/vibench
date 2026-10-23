import os
from dataclasses import dataclass
from functools import lru_cache

import boto3


@dataclass(frozen=True)
class TranslationConfig:
    aws_region: str
    default_source_language: str | None
    default_target_language: str


def load_translation_config() -> TranslationConfig:
    return TranslationConfig(
        aws_region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        default_source_language=os.getenv("TRANSLATION_SOURCE_LANGUAGE"),
        default_target_language=os.getenv("TRANSLATION_TARGET_LANGUAGE", "en"),
    )


@lru_cache(maxsize=1)
def get_aws_translate_client():
    config = load_translation_config()
    return boto3.client("translate", region_name=config.aws_region)


def normalize_language_code(code: str | None) -> str | None:
    if code is None:
        return None
    cleaned = code.strip()
    return cleaned or None
