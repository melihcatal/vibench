from __future__ import annotations

import base64
import os
from typing import Optional

from google.cloud import vision
from openai import OpenAI
import boto3
import deepl
import requests


DEFAULT_GEMINI_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
DEFAULT_OPENAI_TEXT_MODEL = os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini")
DEFAULT_AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def read_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def read_image_base64(image_path: str) -> str:
    return base64.b64encode(read_image_bytes(image_path)).decode("utf-8")


def build_gcv_image(image_path: str) -> vision.Image:
    return vision.Image(content=read_image_bytes(image_path))


def get_google_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))


def get_boto3_client(service_name: str, region_name: Optional[str] = None):
    return boto3.client(service_name, region_name=region_name or DEFAULT_AWS_REGION)


def get_deepl_translator(auth_key: Optional[str] = None) -> deepl.Translator:
    return deepl.Translator(auth_key or os.getenv("DEEPL_AUTH_KEY"))


def perspective_headers() -> dict:
    return {"Content-Type": "application/json"}


def perspective_url() -> str:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    return f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"


def post_json(url: str, payload: dict, headers: Optional[dict] = None) -> dict:
    response = requests.post(url, json=payload, headers=headers or {}, timeout=60)
    response.raise_for_status()
    return response.json()
