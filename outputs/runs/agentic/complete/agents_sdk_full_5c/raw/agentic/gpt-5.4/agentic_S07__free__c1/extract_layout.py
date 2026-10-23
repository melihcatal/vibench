from __future__ import annotations

from document_client import ensure_bytes, get_document_intelligence_client
from document_models import LayoutElement, LayoutResult, polygon_to_bbox


def extract_layout(document_bytes: bytes, model_id: str = "prebuilt-layout") -> LayoutResult:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(model_id=model_id, body=ensure_bytes(document_bytes))
    result = poller.result().as_dict()

    elements = []
    for page in result.get("pages", []):
        page_number = page.get("pageNumber", 1)
        for line in page.get("lines", []):
            elements.append(
                LayoutElement(
                    kind="line",
                    text=line.get("content", ""),
                    page=page_number,
                    confidence=line.get("confidence"),
                    bbox=polygon_to_bbox(line.get("polygon")),
                    meta={"provider": "Azure Document Intelligence"},
                )
            )
    for table in result.get("tables", []):
        region = (table.get("boundingRegions") or [{}])[0]
        elements.append(
            LayoutElement(
                kind="table",
                text=" ".join(cell.get("content", "") for cell in table.get("cells", [])),
                page=region.get("pageNumber", 1),
                bbox=polygon_to_bbox(region.get("polygon")),
                meta={"row_count": table.get("rowCount"), "column_count": table.get("columnCount")},
            )
        )

    return LayoutResult(provider="azure-document-intelligence", elements=elements, raw=result)
