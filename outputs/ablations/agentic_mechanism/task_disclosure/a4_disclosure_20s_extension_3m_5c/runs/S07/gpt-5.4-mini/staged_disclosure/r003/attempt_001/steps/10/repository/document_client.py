import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential


@dataclass(frozen=True)
class DocumentServiceConfig:
    endpoint: str
    api_key: str
    ocr_model: str = "prebuilt-read"
    layout_model: str = "prebuilt-layout"


def load_config() -> DocumentServiceConfig:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT") or os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    api_key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY") or os.getenv("AZURE_FORM_RECOGNIZER_KEY")
    if not endpoint:
        raise ValueError("Missing Azure Document Intelligence endpoint environment variable")
    if not api_key:
        raise ValueError("Missing Azure Document Intelligence key environment variable")
    return DocumentServiceConfig(
        endpoint=endpoint,
        api_key=api_key,
        ocr_model=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_OCR_MODEL", "prebuilt-read"),
        layout_model=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_LAYOUT_MODEL", "prebuilt-layout"),
    )


def create_client(config: Optional[DocumentServiceConfig] = None) -> DocumentAnalysisClient:
    cfg = config or load_config()
    return DocumentAnalysisClient(endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.api_key))


def analyze_ocr(source: Any, config: Optional[DocumentServiceConfig] = None) -> Dict[str, Any]:
    cfg = config or load_config()
    client = create_client(cfg)
    poller = client.begin_analyze_document(cfg.ocr_model, source)
    result = poller.result()
    return result.to_dict()


def analyze_layout(source: Any, config: Optional[DocumentServiceConfig] = None) -> Dict[str, Any]:
    cfg = config or load_config()
    client = create_client(cfg)
    poller = client.begin_analyze_document(cfg.layout_model, source)
    result = poller.result()
    return result.to_dict()
