from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import ensure_endpoint, load_config, require_bytes
from document_models import OCRResult, normalize_text


def extract_text(document: bytes, mime_type: str = "image/png") -> OCRResult:
    config = load_config()
    client = DocumentIntelligenceClient(
        ensure_endpoint(config), AzureKeyCredential(config.api_key or "")
    )
    poller = client.begin_analyze_document(
        "prebuilt-read", require_bytes(document), content_type=mime_type
    )
    result = poller.result()
    text = normalize_text(getattr(result, "content", ""))
    return OCRResult(
        text=text, raw=result.as_dict() if hasattr(result, "as_dict") else None
    )
