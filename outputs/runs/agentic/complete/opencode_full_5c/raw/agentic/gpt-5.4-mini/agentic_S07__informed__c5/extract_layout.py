from document_client import get_document_intelligence_client, get_prebuilt_model_id
from document_models import LayoutExtractionResult


def extract_layout(file_path: str) -> LayoutExtractionResult:
    client = get_document_intelligence_client()
    with open(file_path, "rb") as stream:
        poller = client.begin_analyze_document(
            get_prebuilt_model_id("layout"), body=stream
        )
    result = poller.result()
    elements = []
    for block in getattr(result, "paragraphs", []) or []:
        elements.append(
            {
                "type": "paragraph",
                "content": getattr(block, "content", None),
                "role": getattr(block, "role", None),
            }
        )
    for table in getattr(result, "tables", []) or []:
        elements.append(
            {
                "type": "table",
                "row_count": getattr(table, "row_count", None),
                "column_count": getattr(table, "column_count", None),
            }
        )
    return LayoutExtractionResult(elements=elements)
