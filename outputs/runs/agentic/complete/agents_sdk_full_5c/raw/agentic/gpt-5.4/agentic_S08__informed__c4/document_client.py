from __future__ import annotations

import os
from typing import Any, Dict, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


DEFAULT_API_VERSION = "2024-11-30"


def get_document_intelligence_client(
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> DocumentIntelligenceClient:
    endpoint = endpoint or os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = key or os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        api_version=DEFAULT_API_VERSION,
    )


def read_bytes(path: str) -> bytes:
    with open(path, "rb") as handle:
        return handle.read()


def field_content(field: Any) -> Any:
    if field is None:
        return None
    for attr in ("value_string", "value_date", "value_time", "value_currency", "value_number", "value_integer", "content"):
        if hasattr(field, attr):
            value = getattr(field, attr)
            if value is not None:
                if attr == "value_currency" and hasattr(value, "amount"):
                    return value.amount
                return value
    return getattr(field, "content", None)


def field_confidence(field: Any) -> Optional[float]:
    value = getattr(field, "confidence", None)
    return float(value) if value is not None else None


def model_result_to_dict(result: Any) -> Dict[str, Any]:
    return result.as_dict() if hasattr(result, "as_dict") else {"result": str(result)}
