import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class DocumentClientConfig:
    azure_endpoint: str
    azure_key: str
    azure_api_version: str = "2023-10-31"


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        azure_endpoint=os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"].rstrip("/"),
        azure_key=os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"],
        azure_api_version=os.getenv(
            "AZURE_DOCUMENT_INTELLIGENCE_API_VERSION", "2023-10-31"
        ),
    )


def _headers(cfg: DocumentClientConfig) -> Dict[str, str]:
    return {"Ocp-Apim-Subscription-Key": cfg.azure_key}


def analyze_document(
    model_id: str,
    source_url: Optional[str] = None,
    source_bytes: Optional[bytes] = None,
) -> Dict[str, Any]:
    cfg = load_config()
    url = f"{cfg.azure_endpoint}/formrecognizer/documentModels/{model_id}:analyze?api-version={cfg.azure_api_version}"
    headers = _headers(cfg)
    payload: Dict[str, Any] = {}
    if source_url is not None:
        payload = {"urlSource": source_url}
        headers["Content-Type"] = "application/json"
        response = requests.post(url, headers=headers, json=payload, timeout=120)
    else:
        headers["Content-Type"] = "application/octet-stream"
        response = requests.post(
            url, headers=headers, data=source_bytes or b"", timeout=120
        )
    response.raise_for_status()
    op_location = response.headers.get("operation-location")
    if not op_location:
        return response.json()
    while True:
        poll = requests.get(op_location, headers=_headers(cfg), timeout=120)
        poll.raise_for_status()
        data = poll.json()
        if data.get("status") in {"succeeded", "failed", "canceled"}:
            return data


def get_result_content(result: Dict[str, Any]) -> Dict[str, Any]:
    return result.get("analyzeResult", result)
