from __future__ import annotations

import base64
import os
from typing import Any, Dict

import requests


AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
    "https://example.cognitiveservices.azure.com",
)
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
AZURE_DOCUMENT_INTELLIGENCE_API_VERSION = os.getenv(
    "AZURE_DOCUMENT_INTELLIGENCE_API_VERSION", "2024-11-30"
)
AZURE_DOCUMENT_INTELLIGENCE_MODEL = os.getenv(
    "AZURE_DOCUMENT_INTELLIGENCE_MODEL", "prebuilt-invoice"
)


class AzureDocumentIntelligenceClient:
    def __init__(
        self,
        endpoint: str | None = None,
        api_key: str | None = None,
        api_version: str | None = None,
    ) -> None:
        self.endpoint = (endpoint or AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT).rstrip("/")
        self.api_key = api_key or AZURE_DOCUMENT_INTELLIGENCE_KEY
        self.api_version = api_version or AZURE_DOCUMENT_INTELLIGENCE_API_VERSION
        if not self.api_key:
            raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_KEY is required")

    def analyze_document(
        self, document_bytes: bytes, model_id: str | None = None
    ) -> Dict[str, Any]:
        selected_model = model_id or AZURE_DOCUMENT_INTELLIGENCE_MODEL
        url = f"{self.endpoint}/documentintelligence/documentModels/{selected_model}:analyze?api-version={self.api_version}"
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {"base64Source": base64.b64encode(document_bytes).decode("utf-8")}
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        if "analyzeResult" in data:
            return data
        operation_location = response.headers.get(
            "operation-location"
        ) or response.headers.get("Operation-Location")
        if not operation_location:
            return data
        poll_headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        for _ in range(30):
            poll = requests.get(operation_location, headers=poll_headers, timeout=60)
            poll.raise_for_status()
            poll_data = poll.json()
            if poll_data.get("status") == "succeeded":
                return poll_data
            if poll_data.get("status") in {"failed", "canceled"}:
                raise RuntimeError(
                    f"Document analysis failed with status {poll_data.get('status')}"
                )
        raise TimeoutError("Timed out waiting for Azure Document Intelligence analysis")


def load_document_bytes(source: bytes | str) -> bytes:
    if isinstance(source, bytes):
        return source
    with open(source, "rb") as handle:
        return handle.read()


def extract_analyze_result(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.get("analyzeResult", payload)
