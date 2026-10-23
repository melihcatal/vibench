import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class DocumentExtractionConfig:
    api_key: str
    base_url: str = "https://api.veryfi.com/api/v8/partner/documents"
    username: Optional[str] = None
    model: str = "veryfi-document-extraction"


def load_config() -> DocumentExtractionConfig:
    api_key = os.getenv("VERYFI_API_KEY", "").strip()
    username = os.getenv("VERYFI_USERNAME", "").strip() or None
    base_url = os.getenv("VERYFI_BASE_URL", "https://api.veryfi.com/api/v8/partner/documents").strip()
    model = os.getenv("VERYFI_MODEL", "veryfi-document-extraction").strip()
    if not api_key:
        raise ValueError("VERYFI_API_KEY is required")
    return DocumentExtractionConfig(api_key=api_key, base_url=base_url, username=username, model=model)


class DocumentClient:
    def __init__(self, config: Optional[DocumentExtractionConfig] = None) -> None:
        self.config = config or load_config()
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {self.config.api_key}"})

    def extract(self, document_path: str, extra_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        with open(document_path, "rb") as document_file:
            files = {"file": document_file}
            data: Dict[str, Any] = {"model": self.config.model}
            if self.config.username:
                data["username"] = self.config.username
            if extra_fields:
                data.update(extra_fields)
            response = self._session.post(self.config.base_url, files=files, data=data, timeout=60)
            response.raise_for_status()
            return response.json()

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "DocumentClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
