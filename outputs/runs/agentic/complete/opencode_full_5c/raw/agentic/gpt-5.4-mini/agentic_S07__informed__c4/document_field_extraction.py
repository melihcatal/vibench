import io

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import require_config


def extract_fields(document_bytes: bytes) -> dict:
    cfg = require_config()
    client = DocumentIntelligenceClient(cfg.endpoint, AzureKeyCredential(cfg.key))
    poller = client.begin_analyze_document(
        "prebuilt-invoice", body=io.BytesIO(document_bytes)
    )
    result = poller.result()
    fields = {}
    for name, field in getattr(result, "documents", [{}])[0].fields.items():
        fields[name] = getattr(field, "content", None)
    return fields
