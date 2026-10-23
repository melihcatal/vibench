import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


@dataclass(frozen=True)
class DocumentServiceConfig:
    endpoint: str
    key: str
    ocr_model_id: str = "prebuilt-read"
    layout_model_id: str = "prebuilt-layout"


def load_document_service_config() -> DocumentServiceConfig:
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").strip()
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "").strip()
    if not endpoint:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT is required")
    if not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_KEY is required")
    return DocumentServiceConfig(
        endpoint=endpoint,
        key=key,
        ocr_model_id=os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_OCR_MODEL_ID", "prebuilt-read"),
        layout_model_id=os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_LAYOUT_MODEL_ID", "prebuilt-layout"),
    )


@lru_cache(maxsize=1)
def get_document_intelligence_client() -> DocumentIntelligenceClient:
    config = load_document_service_config()
    return DocumentIntelligenceClient(config.endpoint, AzureKeyCredential(config.key))


def analyze_ocr(document: bytes, content_type: str = "application/pdf") -> Dict[str, Any]:
    config = load_document_service_config()
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(config.ocr_model_id, body=document, content_type=content_type)
    result = poller.result()
    return result.as_dict()


def analyze_layout(document: bytes, content_type: str = "application/pdf") -> Dict[str, Any]:
    config = load_document_service_config()
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(config.layout_model_id, body=document, content_type=content_type)
    result = poller.result()
    return result.as_dict()
