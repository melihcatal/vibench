import os
from typing import Any

from document_models import DocumentExtractionRequest


class DocumentClientConfig:
    def __init__(self) -> None:
        self.endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
        self.key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")


def load_document_request(
    file_path: str = None, content: bytes = None, locale: str = None
) -> DocumentExtractionRequest:
    return DocumentExtractionRequest(
        file_path=file_path, content=content, locale=locale
    )


def read_bytes(request: DocumentExtractionRequest) -> bytes:
    if request.content is not None:
        return request.content
    if request.file_path:
        with open(request.file_path, "rb") as handle:
            return handle.read()
    return b""


def build_azure_client() -> Any:
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.core.credentials import AzureKeyCredential

    cfg = DocumentClientConfig()
    return DocumentIntelligenceClient(cfg.endpoint, AzureKeyCredential(cfg.key))
