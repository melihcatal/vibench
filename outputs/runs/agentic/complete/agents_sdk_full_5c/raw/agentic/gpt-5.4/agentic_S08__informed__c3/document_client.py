from __future__ import annotations

import os
from typing import Any, Dict, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


DEFAULT_MODEL_ID = "prebuilt-invoice"


class DocumentExtractionConfig:
    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        model_id: str = DEFAULT_MODEL_ID,
    ) -> None:
        self.endpoint = endpoint or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.api_key = api_key or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        self.model_id = model_id
        if not self.endpoint:
            raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT is required")
        if not self.api_key:
            raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_KEY is required")



def get_document_client(config: Optional[DocumentExtractionConfig] = None) -> DocumentIntelligenceClient:
    cfg = config or DocumentExtractionConfig()
    return DocumentIntelligenceClient(endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.api_key))



def field_content(field: Any) -> Any:
    if field is None:
        return None
    for attr in ("value_string", "value_date", "value_currency", "value_number", "value_array", "value_object"):
        if hasattr(field, attr):
            value = getattr(field, attr)
            if value is not None:
                if attr == "value_currency" and hasattr(value, "amount"):
                    return value.amount
                return value
    return getattr(field, "content", None)



def field_confidence(field: Any) -> Optional[float]:
    return getattr(field, "confidence", None)



def get_field(fields: Dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in fields:
            return fields[name]
    return None
