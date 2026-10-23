from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

import boto3
from botocore.config import Config
from botocore.client import BaseClient

DEFAULT_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
DEFAULT_BUCKET = os.getenv("OBJECT_STORAGE_BUCKET", "")


@lru_cache(maxsize=1)
def _session() -> boto3.Session:
    return boto3.Session(region_name=DEFAULT_REGION)


@lru_cache(maxsize=1)
def get_s3_client() -> BaseClient:
    return _session().client("s3", config=Config(signature_version="s3v4"))


def get_bucket_name(explicit: Optional[str] = None) -> str:
    bucket = explicit or DEFAULT_BUCKET
    if not bucket:
        raise ValueError("A bucket name must be provided via argument or OBJECT_STORAGE_BUCKET.")
    return bucket


def get_region() -> str:
    return DEFAULT_REGION


def get_s3_resource():
    return _session().resource("s3")


def build_s3_kwargs(extra: Optional[dict] = None) -> dict:
    kwargs = {"region_name": DEFAULT_REGION}
    if extra:
        kwargs.update(extra)
    return kwargs
