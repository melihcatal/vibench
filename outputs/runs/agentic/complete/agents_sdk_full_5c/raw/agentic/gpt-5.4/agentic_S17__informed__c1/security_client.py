from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient
from openai import OpenAI


DEFAULT_AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")


class SecurityConfig:
    def __init__(self) -> None:
        self.aws_region = DEFAULT_AWS_REGION
        self.openai_model = DEFAULT_OPENAI_MODEL
        self.openai_embed_model = DEFAULT_OPENAI_EMBED_MODEL
        self.openai_api_key = os.getenv("OPENAI_API_KEY")


config = SecurityConfig()



def kms_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("kms", region_name=region_name or config.aws_region)



def cloudtrail_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("cloudtrail", region_name=region_name or config.aws_region)



def bedrock_runtime_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("bedrock-runtime", region_name=region_name or config.aws_region)



def translate_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("translate", region_name=region_name or config.aws_region)



def openai_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or config.openai_api_key)
