import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class DocumentClientConfig:
    endpoint: str
    api_key: Optional[str]
    api_version: str
    ocr_model: str
    layout_model: str
    timeout: float


def _env(name: str, default: str = "") -> str:
    value = os.getenv(name)
    return value if value is not None and value != "" else default


def load_document_client_config() -> DocumentClientConfig:
    endpoint = _env("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", _env("DOCUMENT_INTELLIGENCE_ENDPOINT"))
    api_key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY") or os.getenv("DOCUMENT_INTELLIGENCE_KEY")
    api_version = _env("AZURE_DOCUMENT_INTELLIGENCE_API_VERSION", "2024-02-29-preview")
    ocr_model = _env("AZURE_DOCUMENT_INTELLIGENCE_OCR_MODEL", "prebuilt-read")
    layout_model = _env("AZURE_DOCUMENT_INTELLIGENCE_LAYOUT_MODEL", "prebuilt-layout")
    timeout = float(_env("DOCUMENT_INTELLIGENCE_TIMEOUT", "60"))
    return DocumentClientConfig(
        endpoint=endpoint.rstrip("/"),
        api_key=api_key,
        api_version=api_version,
        ocr_model=ocr_model,
        layout_model=layout_model,
        timeout=timeout,
    )


@lru_cache(maxsize=1)
def get_document_client_config() -> DocumentClientConfig:
    return load_document_client_config()


class DocumentIntelligenceClient:
    def __init__(self, config: Optional[DocumentClientConfig] = None) -> None:
        self.config = config or get_document_client_config()
        self._session = requests.Session()
        if self.config.api_key:
            self._session.headers.update({"Ocp-Apim-Subscription-Key": self.config.api_key})

    def analyze(self, model_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.config.endpoint:
            raise ValueError("Missing Azure Document Intelligence endpoint")
        url = f"{self.config.endpoint}/documentintelligence/documentModels/{model_id}:analyze?api-version={self.config.api_version}"
        headers = {"Content-Type": "application/json"}
        response = self._session.post(url, json=payload, headers=headers, timeout=self.config.timeout)
        response.raise_for_status()
        return response.json()

    def ocr(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.analyze(self.config.ocr_model, payload)

    def layout(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.analyze(self.config.layout_model, payload)


def get_document_client(config: Optional[DocumentClientConfig] = None) -> DocumentIntelligenceClient:
    return DocumentIntelligenceClient(config=config)
