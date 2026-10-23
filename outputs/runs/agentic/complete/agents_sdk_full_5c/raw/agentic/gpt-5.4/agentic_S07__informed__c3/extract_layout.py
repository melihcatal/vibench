from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import DEFAULT_LAYOUT_MODEL, get_document_client
from document_models import LayoutElement, LayoutResponse


def extract_layout(document_path: str) -> LayoutResponse:
    client = get_document_client()
    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id=DEFAULT_LAYOUT_MODEL,
            body=AnalyzeDocumentRequest(bytes_source=f.read()),
        )
    result = poller.result()

    elements = []
    for page in result.pages or []:
        for line in page.lines or []:
            polygon = [coord for point in (line.polygon or []) for coord in (point.x, point.y)] if line.polygon else []
            elements.append(
                LayoutElement(
                    kind="line",
                    content=line.content,
                    page_number=page.page_number,
                    polygon=polygon,
                )
            )
        for word in page.words or []:
            polygon = [coord for point in (word.polygon or []) for coord in (point.x, point.y)] if word.polygon else []
            elements.append(
                LayoutElement(
                    kind="word",
                    content=word.content,
                    page_number=page.page_number,
                    confidence=getattr(word, "confidence", None),
                    polygon=polygon,
                )
            )
    for idx, table in enumerate(result.tables or []):
        elements.append(
            LayoutElement(
                kind="table",
                content=f"table_{idx}",
                page_number=(table.bounding_regions[0].page_number if table.bounding_regions else None),
                metadata={"row_count": table.row_count, "column_count": table.column_count},
            )
        )

    return LayoutResponse(elements=elements, provider="azure-document-intelligence", model_id=DEFAULT_LAYOUT_MODEL)
