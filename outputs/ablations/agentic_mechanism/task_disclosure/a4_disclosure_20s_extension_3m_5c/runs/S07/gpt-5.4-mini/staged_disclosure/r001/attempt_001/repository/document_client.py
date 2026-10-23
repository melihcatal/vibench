import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from google.cloud import vision


@dataclass(frozen=True)
class DocumentClientConfig:
    azure_document_intelligence_endpoint: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").rstrip("/")
    azure_document_intelligence_api_key: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_API_KEY", "")
    azure_document_intelligence_api_version: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_API_VERSION", "2024-02-29-preview")
    azure_document_intelligence_model: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_MODEL", "prebuilt-layout")


def get_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def get_document_intelligence_config() -> DocumentClientConfig:
    return DocumentClientConfig()


def read_bytes(source: str) -> bytes:
    path = Path(source)
    return path.read_bytes()


def vision_text_detection(image_path: str, client: Optional[vision.ImageAnnotatorClient] = None) -> str:
    active_client = client or get_vision_client()
    content = read_bytes(image_path)
    image = vision.Image(content=content)
    response = active_client.document_text_detection(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)
    return response.full_text_annotation.text or ""


def document_intelligence_endpoint() -> str:
    return get_document_intelligence_config().azure_document_intelligence_endpoint


def document_intelligence_headers(content_type: str) -> Dict[str, str]:
    config = get_document_intelligence_config()
    if not config.azure_document_intelligence_endpoint or not config.azure_document_intelligence_api_key:
        raise RuntimeError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_API_KEY are required")
    return {
        "Ocp-Apim-Subscription-Key": config.azure_document_intelligence_api_key,
        "Content-Type": content_type,
    }
