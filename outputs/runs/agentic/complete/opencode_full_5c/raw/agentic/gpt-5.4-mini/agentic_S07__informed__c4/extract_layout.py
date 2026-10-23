import io

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import require_config


def extract_layout(document_bytes: bytes):
    cfg = require_config()
    client = DocumentIntelligenceClient(cfg.endpoint, AzureKeyCredential(cfg.key))
    poller = client.begin_analyze_document(
        "prebuilt-layout", body=io.BytesIO(document_bytes)
    )
    result = poller.result()
    return {
        "pages": getattr(result, "pages", []),
        "tables": getattr(result, "tables", []),
        "paragraphs": getattr(result, "paragraphs", []),
        "raw": result,
    }
