from azure.ai.documentintelligence import AnalyzeDocumentRequest

from document_client import create_client
from document_models import LayoutElement, flatten_blocks


def extract_layout(content_bytes: bytes, mime_type: str = "image/png"):
    client = create_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        analyze_request=AnalyzeDocumentRequest(bytes_source=content_bytes),
        content_type=mime_type,
    )
    result = poller.result()
    elements = flatten_blocks(
        getattr(result, "paragraphs", None) or getattr(result, "blocks", None) or []
    )
    return {
        "elements": [
            LayoutElement(kind=e.kind, text=e.text, raw=e.raw).__dict__
            for e in elements
        ],
        "raw": result,
    }
