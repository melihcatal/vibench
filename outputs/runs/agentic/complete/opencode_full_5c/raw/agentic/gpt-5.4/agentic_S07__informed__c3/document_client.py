from __future__ import annotations

import os
from typing import Any

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


DEFAULT_MODEL_ID = "prebuilt-layout"
KEY_VALUE_MODEL_ID = "prebuilt-document"


def get_document_client() -> DocumentIntelligenceClient:
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def analyze_document(
    file_path: str, model_id: str = DEFAULT_MODEL_ID, **kwargs: Any
) -> Any:
    client = get_document_client()
    with open(file_path, "rb") as document:
        poller = client.begin_analyze_document(model_id, body=document, **kwargs)
    return poller.result()
