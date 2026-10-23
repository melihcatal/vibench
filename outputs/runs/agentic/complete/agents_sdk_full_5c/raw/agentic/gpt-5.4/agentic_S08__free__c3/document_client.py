from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

import requests

AZURE_FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT", "")
AZURE_FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY", "")
AZURE_FORM_RECOGNIZER_API_VERSION = os.getenv("AZURE_FORM_RECOGNIZER_API_VERSION", "2024-11-30")
AZURE_FORM_RECOGNIZER_MODEL_INVOICE = "prebuilt-invoice"
AZURE_FORM_RECOGNIZER_MODEL_RECEIPT = "prebuilt-receipt"


class AzureDocumentIntelligenceClient:
    def __init__(self, endpoint: Optional[str] = None, api_key: Optional[str] = None):
        self.endpoint = (endpoint or AZURE_FORM_RECOGNIZER_ENDPOINT).rstrip("/")
        self.api_key = api_key or AZURE_FORM_RECOGNIZER_KEY
        if not self.endpoint:
            raise ValueError("AZURE_FORM_RECOGNIZER_ENDPOINT is required")
        if not self.api_key:
            raise ValueError("AZURE_FORM_RECOGNIZER_KEY is required")

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def analyze_document_url(self, model_id: str, document_url: str) -> Dict[str, Any]:
        url = (
            f"{self.endpoint}/documentintelligence/documentModels/{model_id}:analyze"
            f"?api-version={AZURE_FORM_RECOGNIZER_API_VERSION}"
        )
        response = requests.post(url, headers=self.headers, json={"urlSource": document_url}, timeout=60)
        response.raise_for_status()
        operation_location = response.headers.get("operation-location")
        if not operation_location:
            raise RuntimeError("Azure Document Intelligence did not return operation-location")
        return self._poll(operation_location)

    def analyze_document_bytes(self, model_id: str, content: bytes, content_type: str = "application/pdf") -> Dict[str, Any]:
        url = (
            f"{self.endpoint}/documentintelligence/documentModels/{model_id}:analyze"
            f"?api-version={AZURE_FORM_RECOGNIZER_API_VERSION}"
        )
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": content_type,
        }
        response = requests.post(url, headers=headers, data=content, timeout=60)
        response.raise_for_status()
        operation_location = response.headers.get("operation-location")
        if not operation_location:
            raise RuntimeError("Azure Document Intelligence did not return operation-location")
        return self._poll(operation_location)

    def _poll(self, operation_location: str) -> Dict[str, Any]:
        for _ in range(60):
            result = requests.get(
                operation_location,
                headers={"Ocp-Apim-Subscription-Key": self.api_key},
                timeout=60,
            )
            result.raise_for_status()
            payload = result.json()
            status = payload.get("status")
            if status == "succeeded":
                return payload
            if status == "failed":
                raise RuntimeError(json.dumps(payload))
        raise TimeoutError("Azure Document Intelligence analysis timed out")


def get_first_document(result: Dict[str, Any]) -> Dict[str, Any]:
    analyze_result = result.get("analyzeResult", {})
    documents = analyze_result.get("documents", [])
    if not documents:
        raise ValueError("No documents returned by Azure Document Intelligence")
    return documents[0]


def get_field_value(field: Dict[str, Any]) -> Any:
    if not field:
        return None
    for key in ("valueString", "valueDate", "valueNumber", "valueCurrency", "content", "valueArray", "valueObject"):
        if key in field:
            return field[key]
    return None


def get_field_confidence(field: Dict[str, Any]) -> Optional[float]:
    if not field:
        return None
    confidence = field.get("confidence")
    return float(confidence) if confidence is not None else None
