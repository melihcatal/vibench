import os
from functools import lru_cache

import boto3


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    return default if value is None or value == "" else value


@lru_cache(maxsize=1)
def get_s3_client():
    region = _env("AWS_REGION", _env("AWS_DEFAULT_REGION"))
    kwargs = {}
    if region:
        kwargs["region_name"] = region
    endpoint_url = _env("AWS_S3_ENDPOINT_URL")
    if endpoint_url:
        kwargs["endpoint_url"] = endpoint_url
    return boto3.client("s3", **kwargs)


def default_expires_in() -> int:
    value = _env("S3_PRESIGN_EXPIRES_SECONDS", "3600")
    return int(value)


def default_target_language() -> str:
    return _env("TARGET_LANGUAGE", "en") or "en"


def default_summary_model() -> str:
    return _env("OPENAI_MODEL", "gpt-4o-mini") or "gpt-4o-mini"


def default_embedding_model() -> str:
    return _env("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small") or "text-embedding-3-small"
