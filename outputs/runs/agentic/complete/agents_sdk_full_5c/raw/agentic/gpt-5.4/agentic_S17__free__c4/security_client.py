from __future__ import annotations

import os
from typing import Optional

import boto3
from openai import OpenAI


AWS_REGION_ENV = "AWS_REGION"
AWS_PROFILE_ENV = "AWS_PROFILE"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_BASE_URL_ENV = "OPENAI_BASE_URL"


def get_aws_region() -> str:
    return os.getenv(AWS_REGION_ENV, "us-east-1")


def kms_client(region_name: Optional[str] = None):
    session_kwargs = {}
    profile = os.getenv(AWS_PROFILE_ENV)
    if profile:
        session_kwargs["profile_name"] = profile
    session = boto3.Session(**session_kwargs)
    return session.client("kms", region_name=region_name or get_aws_region())


def cloudtrail_client(region_name: Optional[str] = None):
    session_kwargs = {}
    profile = os.getenv(AWS_PROFILE_ENV)
    if profile:
        session_kwargs["profile_name"] = profile
    session = boto3.Session(**session_kwargs)
    return session.client("cloudtrail", region_name=region_name or get_aws_region())


def openai_client() -> OpenAI:
    kwargs = {"api_key": os.environ[OPENAI_API_KEY_ENV]}
    base_url = os.getenv(OPENAI_BASE_URL_ENV)
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)
