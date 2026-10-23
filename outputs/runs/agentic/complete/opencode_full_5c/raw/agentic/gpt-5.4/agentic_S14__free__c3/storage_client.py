from __future__ import annotations

import os
from functools import lru_cache

import boto3
from botocore.client import BaseClient
from google.cloud import documentai_v1 as documentai
from google.cloud import translate_v3 as translate
from openai import OpenAI


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@lru_cache(maxsize=1)
def get_s3_client() -> BaseClient:
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    session = boto3.session.Session(region_name=region)
    return session.client("s3")


@lru_cache(maxsize=1)
def get_documentai_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


@lru_cache(maxsize=1)
def get_translate_client() -> translate.TranslationServiceClient:
    return translate.TranslationServiceClient()


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    api_key = _required_env("OPENAI_API_KEY")
    return OpenAI(api_key=api_key)


def get_documentai_processor_name() -> str:
    project_id = _required_env("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = _required_env("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"


def get_translate_parent() -> str:
    project_id = _required_env("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_TRANSLATE_LOCATION", "global")
    return f"projects/{project_id}/locations/{location}"
