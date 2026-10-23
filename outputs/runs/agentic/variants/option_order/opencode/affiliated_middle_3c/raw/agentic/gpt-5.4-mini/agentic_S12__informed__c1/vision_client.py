import os
from dataclasses import dataclass
from typing import Optional


def _get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    return value if value else default


def get_dashscope_api_key() -> Optional[str]:
    return _get_env('DASHSCOPE_API_KEY')


def get_openai_api_key() -> Optional[str]:
    return _get_env('OPENAI_API_KEY')


def get_s3_bucket_name() -> Optional[str]:
    return _get_env('VISION_ARCHIVE_BUCKET')
