from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import get_document_intelligence_client, guess_content_type, read_bytes
from document_models import LayoutElement, LayoutResult, normalize_text, polygon_to_dicts


def extract_layout(document_path: str) -> LayoutResult:
    client = get_document_intelligence_client()
    payload = read_bytes(document_path)
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=AnalyzeDocumentRequest(bytes_source=payload),
        content_type=guess_content_type(document_path),
    )
    result = poller.result()

    elements = []

    for page in result.pages or []:
        for line in page.lines or []:
            elements.append(
                LayoutElement(
                    kind="line",
                    text=normalize_text(line.content),
                    page=page.page_number,
                    polygon=polygon_to_dicts(line.polygon),
                )
            )
        for word in page.words or []:
            elements.append(
                LayoutElement(
                    kind="word",
                    text=normalize_text(word.content),
                    page=page.page_number,
                    confidence=word.confidence,
                    polygon=polygon_to_dicts(word.polygon),
                )
            )

    for paragraph in result.paragraphs or []:
        page_number = None
        if paragraph.bounding_regions:
            page_number = paragraph.bounding_regions[0].page_number
        elements.append(
            LayoutElement(
                kind="paragraph",
                text=normalize_text(paragraph.content),
                page=page_number,
                polygon=polygon_to_dicts(paragraph.bounding_regions[0].polygon) if paragraph.bounding_regions else [],
                metadata={"role": getattr(paragraph, "role", None)},
            )
        )

    for table_index, table in enumerate(result.tables or []):
        page_number = None
        polygon = []
        if table.bounding_regions:
            page_number = table.bounding_regions[0].page_number
            polygon = polygon_to_dicts(table.bounding_regions[0].polygon)
        elements.append(
            LayoutElement(
                kind="table",
                text="",
                page=page_number,
                polygon=polygon,
                metadata={
                    "table_index": table_index,
                    "row_count": table.row_count,
                    "column_count": table.column_count,
                },
            )
        )

    return LayoutResult(
        elements=elements,
        provider="azure-ai-documentintelligence:prebuilt-layout",
        raw=result,
    )
