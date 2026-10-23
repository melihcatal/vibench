from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import boto3


@dataclass(frozen=True)
class TranslationClientConfig:
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    region_name: Optional[str] = None
    endpoint_url: Optional[str] = None


def load_translation_config() -> TranslationClientConfig:
    return TranslationClientConfig(
        source_language=os.getenv("TRANSLATION_SOURCE_LANGUAGE"),
        target_language=os.getenv("TRANSLATION_TARGET_LANGUAGE"),
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        endpoint_url=os.getenv("AWS_TRANSLATE_ENDPOINT_URL"),
    )


def get_amazon_translate_client(config: Optional[TranslationClientConfig] = None):
    cfg = config or load_translation_config()
    client_kwargs = {}
    if cfg.region_name:
        client_kwargs["region_name"] = cfg.region_name
    if cfg.endpoint_url:
        client_kwargs["endpoint_url"] = cfg.endpoint_url
    return boto3.client("translate", **client_kwargs)
