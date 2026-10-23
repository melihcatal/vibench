from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from document_models import DocumentRequest, normalize_text_payload

# Provider-identifying signal: OpenAI API
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_DOCUMENT_MODEL", "gpt-4.1-mini")


@dataclass
class DocumentClientConfig:
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = DEFAULT_OPENAI_MODEL
    base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")


class DocumentClient:
    def __init__(self, config: Optional[DocumentClientConfig] = None) -> None:
        self.config = config or DocumentClientConfig()

    def build_request(self, text: str, schema_name: str, metadata: Optional[Dict[str, Any]] = None) -> DocumentRequest:
        return DocumentRequest(
            model=self.config.model,
            schema_name=schema_name,
            text=normalize_text_payload(text),
            metadata=metadata or {},
        )

    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

    def endpoint(self) -> str:
        return f"{self.config.base_url.rstrip('/')}/responses"
