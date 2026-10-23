from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Any

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import vision as google_vision
from openai import OpenAI

AZURE_VISION_ENDPOINT_ENV = "AZURE_VISION_ENDPOINT"
AZURE_VISION_KEY_ENV = "AZURE_VISION_KEY"
AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"
GOOGLE_VISION_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"
GOOGLE_APPLICATION_CREDENTIALS_ENV = "GOOGLE_APPLICATION_CREDENTIALS"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def read_image_bytes(image_path: str | Path) -> bytes:
    return Path(image_path).read_bytes()


def to_data_url(image_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    return f"data:{mime_type};base64,{base64.b64encode(image_bytes).decode('ascii')}"


def get_computer_vision_client() -> ImageAnalysisClient:
    return ImageAnalysisClient(
        endpoint=os.environ[AZURE_VISION_ENDPOINT_ENV],
        credential=AzureKeyCredential(os.environ[AZURE_VISION_KEY_ENV]),
    )


def get_azure_vision_client() -> Any:
    return ImageAnalysisClient(
        endpoint=os.environ[AZURE_CONTENT_SAFETY_ENDPOINT_ENV],
        credential=AzureKeyCredential(os.environ[AZURE_CONTENT_SAFETY_KEY_ENV]),
    )


def get_google_vision_client() -> google_vision.ImageAnnotatorClient:
    return google_vision.ImageAnnotatorClient()


def get_openai_vision_client() -> OpenAI:
    return OpenAI(api_key=os.environ[OPENAI_API_KEY_ENV])
