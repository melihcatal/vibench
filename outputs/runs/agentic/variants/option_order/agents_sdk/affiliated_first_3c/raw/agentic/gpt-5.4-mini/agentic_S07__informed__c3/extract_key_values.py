from __future__ import annotations

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import load_azure_document_intelligence_config
from document_models import KeyValuePair, KeyValueResponse, OCRRequest


def extract_key_values(request: OCRRequest) -> KeyValueResponse:
    config = load_azure_document_intelligence_config()
    client = DocumentIntelligenceClient(endpoint=config.endpoint, credential=AzureKeyCredential(config.key or ""))
    with open(request.document_path, "rb") as handle:
        poller = client.begin_analyze_document("prebuilt-document", body=handle, content_type="application/octet-stream")
    result = poller.result()
    pairs = []
    for kv in getattr(result, "key_value_pairs", []) or []:
        pairs.append(
            KeyValuePair(
                key=getattr(getattr(kv, "key", None), "content", ""),
                value=getattr(getattr(kv, "value", None), "content", ""),
            )
        )
    return KeyValueResponse(pairs=pairs, raw=result)
