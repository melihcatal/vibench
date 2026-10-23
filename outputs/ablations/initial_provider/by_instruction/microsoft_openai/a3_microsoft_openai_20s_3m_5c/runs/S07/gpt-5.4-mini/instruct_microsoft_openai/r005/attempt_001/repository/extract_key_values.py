import json
from typing import Any, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import require_azure_document_intelligence_config
from document_models import DocumentImageRequest, DocumentKeyValueResponse, normalize_analyzed_document


def extract_key_values(request: DocumentImageRequest) -> DocumentKeyValueResponse:
    config = require_azure_document_intelligence_config()
    client = DocumentIntelligenceClient(config.azure_document_intelligence_endpoint, AzureKeyCredential(config.azure_document_intelligence_key))
    with open(request.image_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-document", body=f.read(), content_type=request.content_type)
    result = poller.result()
    raw: Dict[str, Any] = json.loads(json.dumps(result, default=lambda o: getattr(o, "to_dict", lambda: str(o))()))
    normalized = normalize_analyzed_document(raw)
    return DocumentKeyValueResponse(key_values=normalized["keyValuePairs"], raw=raw)
