import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_OPENAI_MODEL = "gpt-4.1-mini"


@dataclass(frozen=True)
class StructuredDocumentConfig:
    api_key: Optional[str] = None
    base_url: str = DEFAULT_OPENAI_BASE_URL
    model: str = DEFAULT_OPENAI_MODEL
    timeout: float = 60.0

    @classmethod
    def from_env(cls) -> "StructuredDocumentConfig":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", DEFAULT_OPENAI_BASE_URL),
            model=os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL),
            timeout=float(os.getenv("OPENAI_TIMEOUT", "60")),
        )


class StructuredDocumentClient:
    def __init__(self, config: Optional[StructuredDocumentConfig] = None) -> None:
        self.config = config or StructuredDocumentConfig.from_env()
        self._session = requests.Session()

    def close(self) -> None:
        self._session.close()

    def extract(self, document_text: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        if not self.config.api_key:
            raise ValueError("OPENAI_API_KEY is required")

        url = self.config.base_url.rstrip("/") + "/responses"
        prompt = (
            "Extract structured data from the provided document text and return only valid JSON "
            "that conforms to the schema. Document text:\n" + document_text
        )
        payload = {
            "model": self.config.model,
            "input": [
                {
                    "role": "system",
                    "content": "You are a structured document extraction assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "structured_document_extraction",
                    "schema": schema,
                    "strict": True,
                }
            },
        }
        response = self._session.post(
            url,
            headers={"Authorization": f"Bearer {self.config.api_key}"},
            json=payload,
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        data = response.json()
        return self._extract_json(data)

    @staticmethod
    def _extract_json(response_data: Dict[str, Any]) -> Dict[str, Any]:
        output = response_data.get("output", [])
        for item in output:
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"}:
                    text = content.get("text", "")
                    if isinstance(text, str) and text.strip():
                        return __import__("json").loads(text)
        if "output_text" in response_data and response_data["output_text"]:
            return __import__("json").loads(response_data["output_text"])
        raise ValueError("No JSON output found in OpenAI response")


def load_default_client() -> StructuredDocumentClient:
    return StructuredDocumentClient()


def extract_document(document_text: str, schema: Dict[str, Any]) -> Dict[str, Any]:
    client = load_default_client()
    try:
        return client.extract(document_text, schema)
    finally:
        client.close()
