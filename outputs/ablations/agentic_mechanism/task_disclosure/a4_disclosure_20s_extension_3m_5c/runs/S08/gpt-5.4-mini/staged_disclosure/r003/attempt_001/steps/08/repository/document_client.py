import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class DocumentClientConfig:
    api_key: str
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-5.4-mini"
    timeout: float = 60.0

    @classmethod
    def from_env(cls) -> "DocumentClientConfig":
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")
        base_url = os.getenv("OPENAI_BASE_URL", cls.base_url).rstrip("/")
        model = os.getenv("OPENAI_MODEL", cls.model).strip() or cls.model
        timeout = float(os.getenv("OPENAI_TIMEOUT", str(cls.timeout)))
        return cls(api_key=api_key, base_url=base_url, model=model, timeout=timeout)


class DocumentClient:
    def __init__(self, config: Optional[DocumentClientConfig] = None) -> None:
        self.config = config or DocumentClientConfig.from_env()
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            }
        )

    def close(self) -> None:
        self._session.close()

    def extract_structured_document(
        self,
        document_text: str,
        schema: Dict[str, Any],
        instructions: str = "Extract the document into the provided JSON schema.",
    ) -> Dict[str, Any]:
        payload = {
            "model": self.config.model,
            "input": [
                {
                    "role": "system",
                    "content": [{"type": "input_text", "text": instructions}],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": document_text},
                        {"type": "input_text", "text": f"Return JSON matching this schema: {schema}"},
                    ],
                },
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": "structured_document", "schema": schema, "strict": True},
            },
        }
        response = self._session.post(
            f"{self.config.base_url}/responses",
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
            if item.get("type") == "message":
                for content in item.get("content", []):
                    if content.get("type") in {"output_text", "text"}:
                        text = content.get("text", "")
                        return _parse_json(text)
        if "output_text" in response_data:
            return _parse_json(response_data["output_text"])
        raise ValueError("No JSON content found in response")


def _parse_json(text: str) -> Dict[str, Any]:
    import json

    return json.loads(text)
