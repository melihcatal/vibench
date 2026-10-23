from __future__ import annotations

from document_client import DEFAULT_MODEL_LAYOUT, OCRClientFactory, load_bytes
from document_models import LayoutElement, LayoutResult, TextSpan, to_bounding_regions


def extract_layout(document_path: str) -> LayoutResult:
    client = OCRClientFactory().create_client()
    poller = client.begin_analyze_document(
        model_id=DEFAULT_MODEL_LAYOUT,
        body=load_bytes(document_path),
        content_type="application/octet-stream",
    )
    result = poller.result()
    elements = []
    for paragraph in result.paragraphs or []:
        elements.append(
            LayoutElement(
                kind="paragraph",
                content=paragraph.content or "",
                bounding_regions=to_bounding_regions(getattr(paragraph, "bounding_regions", None)),
                spans=[TextSpan(offset=s.offset, length=s.length) for s in (paragraph.spans or [])],
                role=getattr(paragraph, "role", None) if False else None,
            )
        )
    for line_page in result.pages or []:
        for line in line_page.lines or []:
            elements.append(
                LayoutElement(
                    kind="line",
                    content=line.content or "",
                    bounding_regions=to_bounding_regions(getattr(line, "bounding_regions", None)),
                    spans=[TextSpan(offset=s.offset, length=s.length) for s in (line.spans or [])],
                )
            )
    for table in result.tables or []:
        elements.append(
            LayoutElement(
                kind="table",
                content=" ".join((cell.content or "") for cell in (table.cells or [])),
                bounding_regions=to_bounding_regions(getattr(table, "bounding_regions", None)),
                metadata={"row_count": table.row_count, "column_count": table.column_count},
            )
        )
    return LayoutResult(content=result.content or "", elements=elements, model_id=DEFAULT_MODEL_LAYOUT)
