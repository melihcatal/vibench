import io
import os

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import require_config
from document_models import as_response


def extract_text(image_bytes: bytes) -> str:
    cfg = require_config()
    client = DocumentIntelligenceClient(cfg.endpoint, AzureKeyCredential(cfg.key))
    poller = client.begin_analyze_document(
        "prebuilt-read", body=io.BytesIO(image_bytes)
    )
    result = poller.result()
    return as_response(getattr(result, "content", ""), raw=result).text
