from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "openai/gpt-5.4-mini"


@dataclass(frozen=True)
class DocumentClientConfig:
    api_key: str
    base_url: str = DEFAULT_OPENAI_BASE_URL
    model: str = DEFAULT_MODEL
    timeout: float = 60.0


def load_document_client_config(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: Optional[str] = None,
    timeout: Optional[float] = None,
) -> DocumentClientConfig:
    resolved_api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
    resolved_base_url = base_url or os.environ.get("OPENAI_BASE_URL", DEFAULT_OPENAI_BASE_URL)
    resolved_model = model or os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)
    resolved_timeout = float(timeout if timeout is not None else os.environ.get("DOCUMENT_CLIENT_TIMEOUT", 60.0))
    if not resolved_api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return DocumentClientConfig(
        api_key=resolved_api_key,
        base_url=resolved_base_url.rstrip("/"),
        model=resolved_model,
        timeout=resolved_timeout,
    )


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

    def close(self) -> None:
        self._session.close()

    def request_json(self, payload: Dict[str, Any], path: str = "/responses") -> Dict[str, Any]:
        body = dict(payload)
        body.setdefault("model", self.config.model)
        response = self._session.post(
            f"{self.config.base_url}{path}",
            json=body,
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        return response.json()
