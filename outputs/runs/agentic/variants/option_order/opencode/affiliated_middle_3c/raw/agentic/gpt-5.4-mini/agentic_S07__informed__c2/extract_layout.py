from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import ensure_endpoint, load_config, require_bytes
from document_models import LayoutResult


def extract_layout(document: bytes, mime_type: str = "image/png") -> LayoutResult:
    config = load_config()
    client = DocumentIntelligenceClient(
        ensure_endpoint(config), AzureKeyCredential(config.api_key or "")
    )
    poller = client.begin_analyze_document(
        "prebuilt-layout", require_bytes(document), content_type=mime_type
    )
    result = poller.result()
    blocks = []
    for paragraph in getattr(result, "paragraphs", []) or []:
        blocks.append(
            {
                "type": "paragraph",
                "content": getattr(paragraph, "content", ""),
                "spans": getattr(paragraph, "spans", []),
            }
        )
    for table in getattr(result, "tables", []) or []:
        blocks.append(
            {
                "type": "table",
                "row_count": getattr(table, "row_count", None),
                "column_count": getattr(table, "column_count", None),
            }
        )
    return LayoutResult(
        blocks=blocks, raw=result.as_dict() if hasattr(result, "as_dict") else None
    )
