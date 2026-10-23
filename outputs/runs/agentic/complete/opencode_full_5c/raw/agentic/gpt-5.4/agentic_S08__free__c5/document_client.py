from __future__ import annotations

import base64
import os
from typing import Any, Dict, Optional

import requests


AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", ""
).rstrip("/")
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
AZURE_DOCUMENT_INTELLIGENCE_API_VERSION = os.getenv(
    "AZURE_DOCUMENT_INTELLIGENCE_API_VERSION", "2024-11-30"
)
AZURE_DOCUMENT_INTELLIGENCE_MODEL = os.getenv(
    "AZURE_DOCUMENT_INTELLIGENCE_MODEL", "prebuilt-invoice"
)


class AzureDocumentIntelligenceClient:
    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        api_version: Optional[str] = None,
    ) -> None:
        self.endpoint = (endpoint or AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT).rstrip("/")
        self.api_key = api_key or AZURE_DOCUMENT_INTELLIGENCE_KEY
        self.api_version = api_version or AZURE_DOCUMENT_INTELLIGENCE_API_VERSION
        if not self.endpoint:
            raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT is required")
        if not self.api_key:
            raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_KEY is required")

    def _headers(self) -> Dict[str, str]:
        return {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def analyze_document(
        self,
        document_bytes: bytes,
        *,
        model_id: Optional[str] = None,
        locale: str = "en-US",
        features: Optional[str] = None,
    ) -> Dict[str, Any]:
        active_model = model_id or AZURE_DOCUMENT_INTELLIGENCE_MODEL
        url = (
            f"{self.endpoint}/documentintelligence/documentModels/{active_model}:analyze"
            f"?api-version={self.api_version}"
        )
        if features:
            url = f"{url}&features={features}"
        payload = {
            "base64Source": base64.b64encode(document_bytes).decode("utf-8"),
            "locale": locale,
        }
        response = requests.post(url, headers=self._headers(), json=payload, timeout=60)
        response.raise_for_status()
        operation_location = response.headers.get("operation-location")
        if not operation_location:
            return response.json()
        return self._poll_result(operation_location)

    def _poll_result(self, operation_location: str) -> Dict[str, Any]:
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        for _ in range(60):
            response = requests.get(operation_location, headers=headers, timeout=60)
            response.raise_for_status()
            body = response.json()
            status = body.get("status")
            if status == "succeeded":
                return body
            if status == "failed":
                raise RuntimeError(
                    f"Azure Document Intelligence analysis failed: {body}"
                )
        raise TimeoutError("Azure Document Intelligence polling timed out")
