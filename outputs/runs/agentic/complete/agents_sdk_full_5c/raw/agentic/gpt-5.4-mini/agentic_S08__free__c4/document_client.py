from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

OPENAI_API_HOST = "https://api.openai.com/v1"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


@dataclass
class DocumentClientConfig:
    api_key: str
    base_url: str = OPENAI_API_HOST
    model: str = OPENAI_MODEL
    timeout: float = 60.0


def load_config() -> DocumentClientConfig:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required for structured document extraction")
    return DocumentClientConfig(
        api_key=api_key,
        base_url=os.getenv("OPENAI_BASE_URL", OPENAI_API_HOST),
        model=os.getenv("OPENAI_MODEL", OPENAI_MODEL),
        timeout=float(os.getenv("OPENAI_TIMEOUT", "60")),
    )


class OpenAIResponsesClient:
    def __init__(self, config: Optional[DocumentClientConfig] = None) -> None:
        self.config = config or load_config()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            }
        )

    def post_json(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.config.base_url}/responses",
            json=payload,
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        return response.json()

    def extract_structured(self, instruction: str, input_text: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "model": self.config.model,
            "input": [
                {"role": "system", "content": instruction},
                {"role": "user", "content": input_text},
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": "document_fields", "schema": schema},
            },
        }
        return self.post_json(payload)
