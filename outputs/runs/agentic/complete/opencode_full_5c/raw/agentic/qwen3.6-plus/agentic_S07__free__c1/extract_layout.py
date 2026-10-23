from __future__ import annotations

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import (
    AnalyzeResult,
    DocumentParagraph,
    DocumentSpan,
)

from document_client import get_document_client, AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
from document_models import (
    DocumentRequest,
    LayoutResult,
    LayoutBlock,
    BoundingBox,
    normalize_confidence,
    normalize_bounding_box,
)

AZURE_LAYOUT_MODEL_ID = "prebuilt-layout"


def _map_block_type(azure_kind: str | None) -> str:
    kind_map = {
        "title": "heading",
        "sectionHeading": "heading",
        "pageHeader": "header",
        "pageFooter": "footer",
        "pageNumber": "page_number",
        "footnote": "footnote",
        "paragraph": "paragraph",
        "listItem": "list_item",
        "selectionMark": "selection_mark",
        "table": "table",
        "formula": "formula",
    }
    return kind_map.get(azure_kind or "", "text")


def extract_layout_from_document(
    request: DocumentRequest,
    client: DocumentIntelligenceClient | None = None,
) -> LayoutResult:
    if client is None:
        client = get_document_client()

    doc_bytes = request.read_bytes()

    poller = client.begin_analyze_document(
        model_id=AZURE_LAYOUT_MODEL_ID,
        body={
            "base64Source": __import__("base64").b64encode(doc_bytes).decode("utf-8")
        },
        output_content_format="text",
    )
    result: AnalyzeResult = poller.result()

    blocks: list[LayoutBlock] = []

    for page_idx, page in enumerate(result.pages or []):
        paragraphs = page.paragraphs or []
        for paragraph in paragraphs:
            role = paragraph.role if hasattr(paragraph, "role") else None
            block_type = _map_block_type(role)
            text = paragraph.content or ""
            confidence = normalize_confidence(paragraph.confidence)
            bbox = normalize_bounding_box(paragraph.polygon)

            blocks.append(
                LayoutBlock(
                    block_type=block_type,
                    text=text,
                    confidence=confidence,
                    bounding_box=bbox,
                    role=role,
                )
            )

        for table in page.tables or []:
            table_text = f"[Table {table.row_count}x{table.column_count}]"
            bbox = normalize_bounding_box(table.polygon)
            blocks.append(
                LayoutBlock(
                    block_type="table",
                    text=table_text,
                    confidence=normalize_confidence(table.confidence),
                    bounding_box=bbox,
                    role="table",
                )
            )

    page_dimensions = result.pages[0] if result.pages else None
    width = page_dimensions.width if page_dimensions else 0.0
    height = page_dimensions.height if page_dimensions else 0.0

    return LayoutResult(
        blocks=blocks,
        page_number=1,
        width=width,
        height=height,
    )


def extract_layout_from_file(
    file_path: str,
    content_type: str = "application/pdf",
) -> LayoutResult:
    request = DocumentRequest.from_file(file_path, content_type)
    return extract_layout_from_document(request)


def extract_layout_from_url(
    url: str,
    client: DocumentIntelligenceClient | None = None,
) -> LayoutResult:
    if client is None:
        client = get_document_client()

    poller = client.begin_analyze_document(
        model_id=AZURE_LAYOUT_MODEL_ID,
        body={"urlSource": url},
        output_content_format="text",
    )
    result: AnalyzeResult = poller.result()

    blocks: list[LayoutBlock] = []

    for page in result.pages or []:
        for paragraph in page.paragraphs or []:
            role = paragraph.role if hasattr(paragraph, "role") else None
            block_type = _map_block_type(role)
            blocks.append(
                LayoutBlock(
                    block_type=block_type,
                    text=paragraph.content or "",
                    confidence=normalize_confidence(paragraph.confidence),
                    bounding_box=normalize_bounding_box(paragraph.polygon),
                    role=role,
                )
            )

    page_dimensions = result.pages[0] if result.pages else None
    width = page_dimensions.width if page_dimensions else 0.0
    height = page_dimensions.height if page_dimensions else 0.0

    return LayoutResult(
        blocks=blocks,
        page_number=1,
        width=width,
        height=height,
    )
