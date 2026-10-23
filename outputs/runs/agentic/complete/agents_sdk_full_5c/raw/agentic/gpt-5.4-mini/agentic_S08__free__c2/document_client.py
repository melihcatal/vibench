from __future__ import annotations

"""Client helpers for structured document extraction integrations."""

import os
from functools import lru_cache

import boto3
from anthropic import Anthropic
from google.cloud import documentai_v1 as documentai
from google.cloud import firestore
from openai import OpenAI


@lru_cache(maxsize=1)
def get_google_documentai_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


@lru_cache(maxsize=4)
def get_aws_textract_client(region_name: str | None = None):
    return boto3.client("textract", region_name=region_name or os.getenv("AWS_REGION", "us-east-1"))


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@lru_cache(maxsize=1)
def get_anthropic_client() -> Anthropic:
    return Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


@lru_cache(maxsize=1)
def get_firestore_client() -> firestore.Client:
    return firestore.Client()
