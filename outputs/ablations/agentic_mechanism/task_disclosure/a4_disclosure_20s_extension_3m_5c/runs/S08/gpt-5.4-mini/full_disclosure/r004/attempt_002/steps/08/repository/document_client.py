from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


DEFAULT_API_BASE = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-5.4-mini"


@dataclass(frozen=True)
class DocumentClientConfig:
    api_key: str
    api_base: str = DEFAULT_API_BASE
    model: str = DEFAULT_MODEL
    timeout_s: float = 60.0


def load_document_client_config() -> DocumentClientConfig:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    api_base = os.environ.get("OPENAI_API_BASE", DEFAULT_API_BASE).strip() or DEFAULT_API_BASE
    model = os.environ.get("OPENAI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    timeout_s = float(os.environ.get("DOCUMENT_EXTRACTION_TIMEOUT_S", "60"))
    return DocumentClientConfig(api_key=api_key, api_base=api_base.rstrip("/"), model=model, timeout_s=timeout_s)


class DocumentExtractionClient:
    def __init__(self, config: Optional[DocumentClientConfig] = None) -> None:
        self.config = config or load_document_client_config()
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            }
        )

    def extract(self, *, text: str, schema: Optional[Dict[str, Any]] = None, instruction: str = "") -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.config.model,
            "input": [
                {
                    "role": "system",
                    "content": [{"type": "input_text", "text": "Extract structured fields from documents."}],
                },
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": self._build_prompt(text=text, instruction=instruction)}],
                },
            ],
        }
        if schema is not None:
            payload["text"] = {"format": {"type": "json_schema", "name": "document_extraction", "schema": schema, "strict": True}}
        response = self._session.post(
            f"{self.config.api_base}/responses",
            data=json.dumps(payload),
            timeout=self.config.timeout_s,
        )
        response.raise_for_status()
        data = response.json()
        return self._parse_response(data)

    def _build_prompt(self, *, text: str, instruction: str) -> str:
        if instruction:
            return f"{instruction}\n\n{text}"
        return text

    def _parse_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        for item in data.get("output", []):
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"} and content.get("text"):
                    text = content["text"]
                    try:
                        return json.loads(text)
                    except Exception:
                        return {"text": text}
        if "output_text" in data:
            try:
                return json.loads(data["output_text"])
            except Exception:
                return {"text": data["output_text"]}
        return data
