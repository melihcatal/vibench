from typing import Any, Dict

import requests

from document_client import get_azure_document_intelligence_endpoint, get_azure_document_intelligence_key
from document_models import DocumentRequest, normalize_table_response


def extract_tables(source: str, language: str = "en") -> Dict[str, Any]:
    request = DocumentRequest(source=source, language=language, features=["tables"])
    endpoint = get_azure_document_intelligence_endpoint()
    key = get_azure_document_intelligence_key()
    with open(request.source, "rb") as handle:
        payload = handle.read()
    url = f"{endpoint}/documentintelligence/documentModels/prebuilt-layout:analyze?api-version=2024-02-29-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/octet-stream"}
    result = requests.post(url, headers=headers, data=payload, timeout=60).json()
    normalized = {"provider": "microsoft-azure-ai-document-intelligence", "tables": result.get("tables", []), "text": result.get("content", ""), "raw": result}
    return normalize_table_response(normalized).__dict__
