from __future__ import annotations

import os
from typing import Optional

import boto3
from openai import OpenAI
from google import genai
import requests
import deepl


DEFAULT_AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def kms_client(region_name: Optional[str] = None):
    return boto3.client("kms", region_name=region_name or DEFAULT_AWS_REGION)


def cloudtrail_client(region_name: Optional[str] = None):
    return boto3.client("cloudtrail", region_name=region_name or DEFAULT_AWS_REGION)


def bedrock_runtime_client(region_name: Optional[str] = None):
    return boto3.client("bedrock-runtime", region_name=region_name or DEFAULT_AWS_REGION)


def openai_client() -> OpenAI:
    return OpenAI(api_key=require_env("OPENAI_API_KEY"))


def gemini_client() -> genai.Client:
    return genai.Client(api_key=require_env("GOOGLE_API_KEY"))


def perspective_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session


def deepl_client() -> deepl.Translator:
    return deepl.Translator(require_env("DEEPL_AUTH_KEY"))
