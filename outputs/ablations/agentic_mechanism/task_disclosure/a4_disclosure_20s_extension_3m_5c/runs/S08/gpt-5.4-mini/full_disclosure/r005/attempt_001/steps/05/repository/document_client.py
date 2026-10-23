import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


DEFAULT_BASE_URL = os.getenv("STRUCTURED_DOCUMENT_EXTRACTION_BASE_URL", "https://api.openai.com")
DEFAULT_API_KEY_ENV = "OPENAI_API_KEY"
DEFAULT_TIMEOUT = float(os.getenv("STRUCTURED_DOCUMENT_EXTRACTION_TIMEOUT", "30"))


@dataclass(frozen=True)
class DocumentClientConfig:
    base_url: str = DEFAULT_BASE_URL
    api_key: Optional[str] = None
    timeout: float = DEFAULT_TIMEOUT

    @classmethod
    def from_env(cls) -> "DocumentClientConfig":
        return cls(
            base_url=os.getenv("STRUCTURED_DOCUMENT_EXTRACTION_BASE_URL", DEFAULT_BASE_URL),
            api_key=os.getenv(DEFAULT_API_KEY_ENV),
            timeout=float(os.getenv("STRUCTURED_DOCUMENT_EXTRACTION_TIMEOUT", str(DEFAULT_TIMEOUT))),
        )


class DocumentClientError(RuntimeError):
    pass


class DocumentClient:
    def __init__(self, config: Optional[DocumentClientConfig] = None) -> None:
        self.config = config or DocumentClientConfig.from_env()
        self._session = requests.Session()

    @property
    def api_key(self) -> str:
        key = self.config.api_key or os.getenv(DEFAULT_API_KEY_ENV)
        if not key:
            raise DocumentClientError(f"Missing API key in {DEFAULT_API_KEY_ENV}")
        return key

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def request(self, method: str, path: str, *, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = self.config.base_url.rstrip("/") + "/" + path.lstrip("/")
        response = self._session.request(
            method=method.upper(),
            url=url,
            headers=self.headers,
            json=json,
            timeout=self.config.timeout,
        )
        if response.status_code >= 400:
            raise DocumentClientError(f"{response.status_code} {response.text}")
        if response.content:
            return response.json()
        return {}

    def close(self) -> None:
        self._session.close()
