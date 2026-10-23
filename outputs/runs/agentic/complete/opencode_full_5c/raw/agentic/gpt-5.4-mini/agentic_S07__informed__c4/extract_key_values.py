import io

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import require_config


def extract_key_values(document_bytes: bytes):
    cfg = require_config()
    client = DocumentIntelligenceClient(cfg.endpoint, AzureKeyCredential(cfg.key))
    poller = client.begin_analyze_document(
        "prebuilt-document", body=io.BytesIO(document_bytes)
    )
    result = poller.result()
    items = []
    for kv in getattr(result, "key_value_pairs", []):
        items.append(
            {
                "key": getattr(getattr(kv, "key", None), "content", ""),
                "value": getattr(getattr(kv, "value", None), "content", ""),
            }
        )
    return items
