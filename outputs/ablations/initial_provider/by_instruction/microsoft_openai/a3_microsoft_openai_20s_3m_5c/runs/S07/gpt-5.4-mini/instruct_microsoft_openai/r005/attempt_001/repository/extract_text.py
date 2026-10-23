import base64
import json
import os
from typing import Any, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import require_azure_document_intelligence_config
from document_models import DocumentImageRequest, DocumentTextResponse, normalize_analyzed_document


def _load_bytes(request: DocumentImageRequest) -> bytes:
    if request.image_path:
        with open(request.image_path, "rb") as f:
            return f.read()
    if request.image_url and request.image_url.startswith("data:"):
        return base64.b64decode(request.image_url.split(",", 1)[1])
    raise ValueError("image_path or data URL image_url required")


def extract_text(request: DocumentImageRequest) -> DocumentTextResponse:
    config = require_azure_document_intelligence_config()
    client = DocumentIntelligenceClient(config.azure_document_intelligence_endpoint, AzureKeyCredential(config.azure_document_intelligence_key))
    data = _load_bytes(request)
    poller = client.begin_analyze_document("prebuilt-read", body=data, content_type=request.content_type)
    result = poller.result()
    raw: Dict[str, Any] = json.loads(json.dumps(result, default=lambda o: getattr(o, "to_dict", lambda: str(o))()))
    normalized = normalize_analyzed_document(raw)
    return DocumentTextResponse(text=normalized["content"], raw=raw)
