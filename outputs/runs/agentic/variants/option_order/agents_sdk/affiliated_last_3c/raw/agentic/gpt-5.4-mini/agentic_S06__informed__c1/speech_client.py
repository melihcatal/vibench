from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.client import BaseClient


@dataclass(frozen=True)
class SpeechConfig:
    region: str
    voice_id: str = "Joanna"
    engine: str = "neural"
    output_format: str = "mp3"


@lru_cache(maxsize=1)
def load_config() -> SpeechConfig:
    return SpeechConfig(
        region=os.getenv("AWS_DEFAULT_REGION", os.getenv("AWS_REGION", "us-east-1")),
        voice_id=os.getenv("POLLY_VOICE_ID", "Joanna"),
        engine=os.getenv("POLLY_ENGINE", "neural"),
        output_format=os.getenv("POLLY_OUTPUT_FORMAT", "mp3"),
    )


@lru_cache(maxsize=1)
def get_polly_client(region: Optional[str] = None) -> BaseClient:
    cfg = load_config()
    return boto3.client("polly", region_name=region or cfg.region)


def normalize_voice_id(voice_id: Optional[str] = None) -> str:
    return voice_id or load_config().voice_id


def normalize_output_format(output_format: Optional[str] = None) -> str:
    return output_format or load_config().output_format


def normalize_engine(engine: Optional[str] = None) -> str:
    return engine or load_config().engine
