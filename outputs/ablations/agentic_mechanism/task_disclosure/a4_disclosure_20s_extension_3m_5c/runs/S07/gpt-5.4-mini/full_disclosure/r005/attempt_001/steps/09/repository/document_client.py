import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class DocumentServiceConfig:
    api_key: Optional[str] = None
    base_url: str = "https://api.veryfi.com/api/v7"
    timeout: float = 60.0

    @classmethod
    def from_env(cls) -> "DocumentServiceConfig":
        return cls(
            api_key=os.getenv("VERYFI_API_KEY"),
            base_url=os.getenv("VERYFI_BASE_URL", "https://api.veryfi.com/api/v7"),
            timeout=float(os.getenv("VERYFI_TIMEOUT", "60")),
        )


class DocumentClient:
    def __init__(self, config: Optional[DocumentServiceConfig] = None) -> None:
        self.config = config or DocumentServiceConfig.from_env()
        self._session = requests.Session()
        self._session.headers.update({"Accept": "application/json"})
        if self.config.api_key:
            self._session.headers.update({"Authorization": f"apikey {self.config.api_key}"})

    def _request(self, method: str, path: str, **kwargs: Any) -> Dict[str, Any]:
        url = f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"
        response = self._session.request(method, url, timeout=self.config.timeout, **kwargs)
        response.raise_for_status()
        if response.content:
            return response.json()
        return {}

    def extract_text(self, image_bytes: bytes, filename: str = "document") -> Dict[str, Any]:
        files = {"file": (filename, image_bytes)}
        return self._request("POST", "/partner/documents", files=files)

    def extract_layout(self, image_bytes: bytes, filename: str = "document") -> Dict[str, Any]:
        files = {"file": (filename, image_bytes)}
        params = {"fields": "layout"}
        return self._request("POST", "/partner/documents", files=files, params=params)

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "DocumentClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def get_document_client() -> DocumentClient:
    return DocumentClient()
