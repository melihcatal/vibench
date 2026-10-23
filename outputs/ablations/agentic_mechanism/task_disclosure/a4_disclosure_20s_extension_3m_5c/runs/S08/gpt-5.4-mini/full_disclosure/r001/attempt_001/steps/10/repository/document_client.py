from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

import requests


DEFAULT_API_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-5.4-mini"


def _load_json_file(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def _first_nonempty(*values: Optional[str]) -> Optional[str]:
    for value in values:
        if value is not None and str(value).strip():
            return str(value).strip()
    return None


@dataclass(frozen=True)
class DocumentClientConfig:
    api_key: str
    api_base_url: str = DEFAULT_API_BASE_URL
    model: str = DEFAULT_MODEL
    timeout_seconds: float = 60.0

    @classmethod
    def from_env(cls) -> "DocumentClientConfig":
        config_path = os.getenv("DOCUMENT_EXTRACTION_CONFIG")
        file_config: Dict[str, Any] = _load_json_file(Path(config_path)) if config_path else {}

        api_key = _first_nonempty(
            os.getenv("OPENAI_API_KEY"),
            os.getenv("DOCUMENT_EXTRACTION_API_KEY"),
            file_config.get("api_key"),
        )
        if not api_key:
            raise ValueError("Missing API key: set OPENAI_API_KEY or DOCUMENT_EXTRACTION_API_KEY")

        api_base_url = _first_nonempty(
            os.getenv("OPENAI_BASE_URL"),
            os.getenv("DOCUMENT_EXTRACTION_API_BASE_URL"),
            file_config.get("api_base_url"),
            DEFAULT_API_BASE_URL,
        ) or DEFAULT_API_BASE_URL

        model = _first_nonempty(
            os.getenv("DOCUMENT_EXTRACTION_MODEL"),
            file_config.get("model"),
            DEFAULT_MODEL,
        ) or DEFAULT_MODEL

        timeout_raw = _first_nonempty(
            os.getenv("DOCUMENT_EXTRACTION_TIMEOUT"),
            file_config.get("timeout_seconds"),
        )
        timeout_seconds = float(timeout_raw) if timeout_raw else 60.0

        return cls(api_key=api_key, api_base_url=api_base_url.rstrip("/"), model=model, timeout_seconds=timeout_seconds)


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

    def __enter__(self) -> "DocumentClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def request(self, payload: Mapping[str, Any], *, endpoint: str = "/responses") -> Dict[str, Any]:
        url = f"{self.config.api_base_url}{endpoint}"
        body = dict(payload)
        body.setdefault("model", self.config.model)
        response = self._session.post(url, json=body, timeout=self.config.timeout_seconds)
        response.raise_for_status()
        return response.json()


def get_document_client(config: Optional[DocumentClientConfig] = None) -> DocumentClient:
    return DocumentClient(config=config)


def load_local_config(path: Optional[str] = None) -> Dict[str, Any]:
    config_path = Path(path or os.getenv("DOCUMENT_EXTRACTION_CONFIG", "")).expanduser()
    return _load_json_file(config_path) if str(config_path) else {}


def normalize_response_text(response: Mapping[str, Any]) -> str:
    if "output_text" in response and isinstance(response["output_text"], str):
        return response["output_text"]
    output = response.get("output")
    if isinstance(output, list):
        chunks = []
        for item in output:
            if isinstance(item, Mapping):
                content = item.get("content")
                if isinstance(content, list):
                    for part in content:
                        if isinstance(part, Mapping) and isinstance(part.get("text"), str):
                            chunks.append(part["text"])
        return "".join(chunks)
    return ""
