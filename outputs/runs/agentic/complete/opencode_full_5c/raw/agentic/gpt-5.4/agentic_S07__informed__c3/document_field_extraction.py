from __future__ import annotations

import os

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def extract_document_fields(file_path: str) -> dict:
    client = DocumentIntelligenceClient(
        endpoint=os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"],
        credential=AzureKeyCredential(os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]),
    )
    with open(file_path, "rb") as document:
        poller = client.begin_analyze_document("prebuilt-invoice", body=document)
    result = poller.result()
    documents = []
    for doc in getattr(result, "documents", None) or []:
        fields = {}
        for name, value in (getattr(doc, "fields", None) or {}).items():
            fields[name] = {
                "value": getattr(value, "value", None),
                "content": getattr(value, "content", None),
                "confidence": getattr(value, "confidence", None),
            }
        documents.append({"doc_type": getattr(doc, "doc_type", None), "fields": fields})
    return {
        "provider": "azure_document_intelligence",
        "model_id": "prebuilt-invoice",
        "documents": documents,
    }
