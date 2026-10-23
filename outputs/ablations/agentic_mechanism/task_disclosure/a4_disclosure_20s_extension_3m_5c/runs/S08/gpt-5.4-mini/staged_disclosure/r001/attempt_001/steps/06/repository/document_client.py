import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class DocumentExtractionConfig:
    api_key: str
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-5.4-mini"
    timeout: float = 60.0


def load_config(env: Optional[Dict[str, str]] = None) -> DocumentExtractionConfig:
    source = env if env is not None else os.environ
    api_key = source.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    base_url = source.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = source.get("OPENAI_MODEL", "gpt-5.4-mini").strip() or "gpt-5.4-mini"
    timeout_raw = source.get("OPENAI_TIMEOUT", "60").strip()
    try:
        timeout = float(timeout_raw)
    except ValueError as exc:
        raise ValueError("OPENAI_TIMEOUT must be a number") from exc
    return DocumentExtractionConfig(api_key=api_key, base_url=base_url, model=model, timeout=timeout)


class DocumentClient:
    def __init__(self, config: Optional[DocumentExtractionConfig] = None) -> None:
        self.config = config or load_config()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            }
        )

    def extract_structured_document(self, text: str, schema: Dict[str, Any], temperature: float = 0.0) -> Dict[str, Any]:
        payload = {
            "model": self.config.model,
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Extract structured data from the provided document and return only valid JSON matching the supplied schema.",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": text},
                    ],
                },
            ],
            "temperature": temperature,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_document_extraction",
                    "schema": schema,
                    "strict": True,
                },
            },
        }
        response = self.session.post(
            f"{self.config.base_url}/responses",
            json=payload,
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        data = response.json()
        return data
