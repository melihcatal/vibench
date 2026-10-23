import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class StructuredDocumentClientConfig:
    api_key: str
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-5.4-mini"
    timeout: float = 60.0


def load_client_config(env: Optional[Dict[str, str]] = None) -> StructuredDocumentClientConfig:
    source = env if env is not None else os.environ
    api_key = source.get("OPENAI_API_KEY", "")
    base_url = source.get("STRUCTURED_DOCUMENT_BASE_URL", "https://api.openai.com/v1")
    model = source.get("STRUCTURED_DOCUMENT_MODEL", "gpt-5.4-mini")
    timeout_value = source.get("STRUCTURED_DOCUMENT_TIMEOUT", "60")
    try:
        timeout = float(timeout_value)
    except (TypeError, ValueError):
        timeout = 60.0
    return StructuredDocumentClientConfig(api_key=api_key, base_url=base_url.rstrip("/"), model=model, timeout=timeout)


class StructuredDocumentClient:
    def __init__(self, config: Optional[StructuredDocumentClientConfig] = None):
        self.config = config or load_client_config()

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def post_json(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.config.base_url}/{path.lstrip('/')}"
        response = requests.post(url, headers=self._headers(), json=payload, timeout=self.config.timeout)
        response.raise_for_status()
        return response.json()

    def chat_completion(self, messages: Any, **kwargs: Any) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"model": kwargs.pop("model", self.config.model), "messages": messages}
        payload.update(kwargs)
        return self.post_json("chat/completions", payload)
