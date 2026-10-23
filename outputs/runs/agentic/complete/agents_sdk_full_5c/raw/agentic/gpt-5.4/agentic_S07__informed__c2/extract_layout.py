from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import DEFAULT_LAYOUT_MODEL, get_document_client, load_document_bytes
from document_models import LayoutBlock, LayoutResult, azure_paragraph_kind


def extract_layout(document_path: str, model_id: str = DEFAULT_LAYOUT_MODEL) -> LayoutResult:
    client = get_document_client()
    body = AnalyzeDocumentRequest(bytes_source=load_document_bytes(document_path))
    poller = client.begin_analyze_document(model_id=model_id, body=body)
    result = poller.result()

    blocks = []

    for paragraph in result.paragraphs or []:
        region = (getattr(paragraph, "bounding_regions", None) or [None])[0]
        blocks.append(
            LayoutBlock(
                kind=azure_paragraph_kind(paragraph),
                content=getattr(paragraph, "content", "") or "",
                page_number=getattr(region, "page_number", None) if region else None,
                polygon=list(getattr(region, "polygon", []) or []) if region else [],
            )
        )

    for page in result.pages or []:
        for line in page.lines or []:
            blocks.append(
                LayoutBlock(
                    kind="line",
                    content=getattr(line, "content", "") or "",
                    page_number=getattr(page, "page_number", None),
                    polygon=list(getattr(line, "polygon", []) or []),
                )
            )

    for table in result.tables or []:
        region = (getattr(table, "bounding_regions", None) or [None])[0]
        summary = f"table[{getattr(table, 'row_count', 0)}x{getattr(table, 'column_count', 0)}]"
        blocks.append(
            LayoutBlock(
                kind="table",
                content=summary,
                page_number=getattr(region, "page_number", None) if region else None,
                polygon=list(getattr(region, "polygon", []) or []) if region else [],
            )
        )

    return LayoutResult(blocks=blocks, provider="azure-document-intelligence", model_id=model_id)
