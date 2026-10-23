import os
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class DocumentServiceConfig:
    endpoint: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
    api_key: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
    api_version: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_API_VERSION", "2024-02-29-preview")


def get_config() -> DocumentServiceConfig:
    return DocumentServiceConfig()


def _headers(config: DocumentServiceConfig) -> dict:
    return {"Ocp-Apim-Subscription-Key": config.api_key, "Content-Type": "application/json"}


def analyze_document(model_id: str, document_url: str, features: Optional[str] = None) -> dict:
    config = get_config()
    payload = {"urlSource": document_url}
    if features:
        payload["features"] = features
    response = requests.post(
        f"{config.endpoint}/documentintelligence/documentModels/{model_id}:analyze?api-version={config.api_version}",
        headers=_headers(config),
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def get_analyze_result(operation_location: str) -> dict:
    config = get_config()
    response = requests.get(operation_location, headers={"Ocp-Apim-Subscription-Key": config.api_key}, timeout=120)
    response.raise_for_status()
    return response.json()
