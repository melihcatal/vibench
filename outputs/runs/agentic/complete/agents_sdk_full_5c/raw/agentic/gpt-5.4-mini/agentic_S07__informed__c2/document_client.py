from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_models import DocumentInput


@dataclass
class DocumentServiceConfig:
    endpoint: str
    key: str
    model_id: str = "prebuilt-layout"


def load_config(model_id: str = "prebuilt-layout") -> DocumentServiceConfig:
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentServiceConfig(endpoint=endpoint, key=key, model_id=model_id)


def get_client(config: Optional[DocumentServiceConfig] = None) -> DocumentIntelligenceClient:
    config = config or load_config()
    return DocumentIntelligenceClient(endpoint=config.endpoint, credential=AzureKeyCredential(config.key))


def analyze_document(client: DocumentIntelligenceClient, document: DocumentInput, model_id: str = "prebuilt-layout") -> Any:
    poller = client.begin_analyze_document(
        model_id=model_id,
        body=document.content,
        content_type=document.mime_type,
        locale=document.language_hints[0] if document.language_hints else None,
    )
    return poller.result()
