import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


DEFAULT_API_BASE = "https://api.anthropic.com"
DEFAULT_MODEL = "claude-3-5-sonnet-20241022"


@dataclass(frozen=True)
class DocumentClientConfig:
    api_key: str
    api_base: str = DEFAULT_API_BASE
    model: str = DEFAULT_MODEL
    timeout: float = 60.0


def load_document_client_config() -> DocumentClientConfig:
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is required")
    api_base = os.getenv("ANTHROPIC_API_BASE", DEFAULT_API_BASE).strip() or DEFAULT_API_BASE
    model = os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    timeout = float(os.getenv("ANTHROPIC_TIMEOUT", "60"))
    return DocumentClientConfig(api_key=api_key, api_base=api_base, model=model, timeout=timeout)


class DocumentClient:
    def __init__(self, config: Optional[DocumentClientConfig] = None) -> None:
        self.config = config or load_document_client_config()

    def extract_structured_document(self, text: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.config.api_base.rstrip('/')}/v1/messages"
        headers = {
            "x-api-key": self.config.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": self.config.model,
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Extract structured data from the following document according to this JSON schema:\n{schema}\n\nDocument:\n{text}",
                        }
                    ],
                }
            ],
        }
        response = requests.post(url, headers=headers, json=payload, timeout=self.config.timeout)
        response.raise_for_status()
        return response.json()
