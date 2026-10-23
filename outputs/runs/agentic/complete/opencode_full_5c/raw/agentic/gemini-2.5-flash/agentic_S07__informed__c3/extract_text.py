from document_client import get_document_intelligence_client
from document_models import ExtractedText
import io


def extract_text_from_document(document_content: bytes) -> ExtractedText:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        "prebuilt-document", document_content, content_type="application/octet-stream"
    )
    result = poller.result()
    return ExtractedText(content=result.content)
