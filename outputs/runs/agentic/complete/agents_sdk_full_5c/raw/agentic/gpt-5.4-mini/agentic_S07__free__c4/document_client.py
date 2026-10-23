import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

AZURE_FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT", "")
AZURE_FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY", "")
AZURE_FORM_RECOGNIZER_API_VERSION = os.getenv("AZURE_FORM_RECOGNIZER_API_VERSION", "2024-11-30")


@dataclass
class DocumentClientConfig:
    endpoint: str
    api_key: str
    api_version: str = AZURE_FORM_RECOGNIZER_API_VERSION


class DocumentClientError(RuntimeError):
    pass


class AzureDocumentIntelligenceClient:
    def __init__(self, config: Optional[DocumentClientConfig] = None):
        self.config = config or DocumentClientConfig(
            endpoint=AZURE_FORM_RECOGNIZER_ENDPOINT,
            api_key=AZURE_FORM_RECOGNIZER_KEY,
        )
        if not self.config.endpoint or not self.config.api_key:
            raise DocumentClientError("Azure Document Intelligence configuration is required")

    @property
    def base_url(self) -> str:
        return self.config.endpoint.rstrip("/")

    def headers(self) -> Dict[str, str]:
        return {
            "Ocp-Apim-Subscription-Key": self.config.api_key,
            "Content-Type": "application/json",
        }

    def post_analyze(self, model_id: str, payload: Dict[str, Any]) -> requests.Response:
        url = f"{self.base_url}/documentintelligence/documentModels/{model_id}:analyze?api-version={self.config.api_version}"
        return requests.post(url, headers=self.headers(), json=payload, timeout=60)

    def get_operation(self, operation_url: str) -> requests.Response:
        return requests.get(operation_url, headers=self.headers(), timeout=60)


def get_default_client() -> AzureDocumentIntelligenceClient:
    return AzureDocumentIntelligenceClient()
