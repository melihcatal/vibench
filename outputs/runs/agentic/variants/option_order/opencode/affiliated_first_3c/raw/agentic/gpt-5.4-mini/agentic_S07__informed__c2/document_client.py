import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_document_intelligence_client(
    endpoint: Optional[str] = None, key: Optional[str] = None
) -> DocumentIntelligenceClient:
    endpoint = endpoint or os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = key or os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def get_model_id(name: str) -> str:
    mapping = {
        "ocr": "prebuilt-read",
        "layout": "prebuilt-layout",
        "tables": "prebuilt-layout",
        "kv": "prebuilt-document",
        "invoice": "prebuilt-invoice",
    }
    return mapping.get(name, "prebuilt-layout")
