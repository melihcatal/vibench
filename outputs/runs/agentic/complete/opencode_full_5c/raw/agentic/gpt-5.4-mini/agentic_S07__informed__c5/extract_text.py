from document_client import get_document_intelligence_client, get_prebuilt_model_id
from document_models import (
    DocumentRequest,
    TextExtractionResult,
    normalize_document_result,
)


def extract_text(file_path: str) -> TextExtractionResult:
    client = get_document_intelligence_client()
    with open(DocumentRequest(file_path).file_path, "rb") as stream:
        poller = client.begin_analyze_document(
            get_prebuilt_model_id("ocr"), body=stream
        )
    result = poller.result()
    content = getattr(result, "content", "") or ""
    return TextExtractionResult(text=content, pages=normalize_document_result(result))
