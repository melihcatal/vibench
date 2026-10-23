import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class DocumentClientConfig:
    endpoint: str
    api_key: str
    model: str = "prebuilt-invoice"


def load_document_client_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        endpoint=os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", ""),
        api_key=os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", ""),
    )


def build_azure_document_intelligence_client() -> Any:
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.core.credentials import AzureKeyCredential

    config = load_document_client_config()
    return DocumentIntelligenceClient(
        config.endpoint, AzureKeyCredential(config.api_key)
    )


def normalize_azure_pages(result: Any) -> Dict[str, Any]:
    pages = []
    for page in getattr(result, "pages", []) or []:
        pages.append(
            {
                "page_number": getattr(page, "page_number", None),
                "width": getattr(page, "width", None),
                "height": getattr(page, "height", None),
            }
        )
    return {"pages": pages}


def field_value_to_python(value: Any) -> Any:
    for attr in ("value", "content", "text"):
        if hasattr(value, attr):
            v = getattr(value, attr)
            if v is not None:
                return v
    return value
