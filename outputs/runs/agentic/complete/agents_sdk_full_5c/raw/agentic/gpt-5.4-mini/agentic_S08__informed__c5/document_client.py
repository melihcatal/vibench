from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


@dataclass(frozen=True)
class DocumentExtractionConfig:
    endpoint: str
    key: str

    @classmethod
    def from_env(cls) -> "DocumentExtractionConfig":
        endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").strip()
        key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "").strip()
        if not endpoint or not key:
            raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")
        return cls(endpoint=endpoint, key=key)


class DocumentClientHelper:
    def __init__(self, config: Optional[DocumentExtractionConfig] = None) -> None:
        self.config = config or DocumentExtractionConfig.from_env()
        self.client = DocumentIntelligenceClient(self.config.endpoint, AzureKeyCredential(self.config.key))

    def analyze_from_url(self, model_id: str, url: str) -> Dict[str, Any]:
        poller = self.client.begin_analyze_document(model_id, {"urlSource": url})
        result = poller.result()
        return result.to_dict() if hasattr(result, "to_dict") else result

    def analyze_from_bytes(self, model_id: str, content: bytes) -> Dict[str, Any]:
        poller = self.client.begin_analyze_document(model_id, content)
        result = poller.result()
        return result.to_dict() if hasattr(result, "to_dict") else result
