"""
[SAME-SCENARIO] Extracts blocks, lines, tables, or layout elements from a document.

Provider: Google Document AI (google-cloud-documentai)
Auth: GOOGLE_APPLICATION_CREDENTIALS
Model/Processor: Built-in Layout parser processor for document layout analysis
"""

from __future__ import annotations

import os
from typing import Optional, List, Dict, Any

from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai
from google.cloud.documentai_v1.types import document as documentai_types

from document_client import load_image_bytes, get_google_project_id
from document_models import (
    LayoutBlock,
    OcrLine,
    OcrWord,
    TableStructure,
    TableCell,
    BoundingBox,
    OcrDocumentResult,
)


LAYOUT_TYPE_MAP = {
    "paragraph": "paragraph",
    "heading_1": "heading",
    "heading_2": "heading",
    "heading_3": "heading",
    "heading_4": "heading",
    "heading_5": "heading",
    "heading_6": "heading",
    "header": "header",
    "footer": "footer",
    "footnote": "footnote",
    "text": "text",
    "list_item": "list_item",
    "table": "table",
    "form": "form",
    "key_value_region": "key_value",
    "title": "title",
    "equation": "equation",
    "caption": "caption",
    "page_number": "page_number",
}


def extract_layout_from_document(
    file_path: str,
    project_id: Optional[str] = None,
    location: str = "us",
    processor_id: Optional[str] = None,
    mime_type: Optional[str] = None,
) -> OcrDocumentResult:
    """
    Extract layout blocks, lines, and table structures from a document using
    Google Document AI Layout processor (documentai.googleapis.com).

    Returns an OcrDocumentResult with populated blocks, lines, and tables.
    """
    project_id = project_id or get_google_project_id()
    if not project_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT environment variable or project_id argument is required"
        )

    processor_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    client_options = ClientOptions(
        api_endpoint=f"{location}-documentai.googleapis.com"
    )

    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    raw_bytes = load_image_bytes(file_path)
    if mime_type is None:
        ext = os.path.splitext(file_path)[1].lower()
        mime_type = "application/pdf" if ext == ".pdf" else "image/png"

    raw_document = documentai.RawDocument(
        content=raw_bytes,
        mime_type=mime_type,
    )

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    result = client.process_document(request=request)
    document = result.document
    full_text = document.text

    blocks: List[LayoutBlock] = []
    all_lines: List[OcrLine] = []
    tables: List[TableStructure] = []
    page_count = len(document.pages)

    for page in document.pages:
        page_blocks = _extract_page_blocks(page, full_text)
        blocks.extend(page_blocks)

        page_lines = _extract_page_lines(page, full_text)
        all_lines.extend(page_lines)

        page_tables = _extract_page_tables(page, full_text)
        tables.extend(page_tables)

    return OcrDocumentResult(
        plain_text=full_text,
        blocks=blocks,
        lines=all_lines,
        tables=tables,
        page_count=page_count,
    )


def _extract_page_blocks(
    page: documentai_types.Document.Page,
    full_text: str,
) -> List[LayoutBlock]:
    """Extract layout blocks from a single page."""
    blocks: List[LayoutBlock] = []

    for para in page.paragraphs:
        text = _text_from_layout(para.layout, full_text)
        bbox = _bbox_from_layout(para.layout)
        blocks.append(
            LayoutBlock(
                block_type="paragraph",
                text=text,
                confidence=1.0,
                bounding_box=bbox,
            )
        )

    for block_type_attr in ("headers", "footers"):
        elements = getattr(page, block_type_attr, [])
        for elem in elements:
            text = _text_from_layout(elem.layout, full_text)
            bbox = _bbox_from_layout(elem.layout)
            blocks.append(
                LayoutBlock(
                    block_type=block_type_attr,
                    text=text,
                    confidence=1.0,
                    bounding_box=bbox,
                )
            )

    for elem in getattr(page, "form_fields", []):
        name_text = ""
        value_text = ""
        if elem.field_name and elem.field_name.text_anchor:
            name_text = _text_from_text_anchor(elem.field_name.text_anchor, full_text)
        if elem.field_value and elem.field_value.text_anchor:
            value_text = _text_from_text_anchor(elem.field_value.text_anchor, full_text)
        blocks.append(
            LayoutBlock(
                block_type="form_field",
                text=f"{name_text}: {value_text}",
                confidence=1.0,
            )
        )

    return blocks


def _extract_page_lines(
    page: documentai_types.Document.Page,
    full_text: str,
) -> List[OcrLine]:
    """Extract lines and words from a page."""
    lines: List[OcrLine] = []
    for line in page.lines:
        line_text = _text_from_layout(line.layout, full_text)
        words: List[OcrWord] = []
        for token in line.tokens:
            token_text = _text_from_layout(token.layout, full_text)
            token_conf = 0.0
            if token.detected_languages:
                token_conf = token.detected_languages[0].confidence
            words.append(OcrWord(text=token_text, confidence=token_conf))
        bbox = _bbox_from_layout(line.layout)
        lines.append(
            OcrLine(text=line_text, words=words, confidence=1.0, bounding_box=bbox)
        )
    return lines


def _extract_page_tables(
    page: documentai_types.Document.Page,
    full_text: str,
) -> List[TableStructure]:
    """Extract table structures from a page."""
    tables: List[TableStructure] = []
    for table in page.tables:
        cells: List[TableCell] = []
        row_count = table.body_rows if hasattr(table, "body_rows") else len(table.header_rows) + 1
        col_count = table.col_count if hasattr(table, "col_count") else 0
        if not col_count:
            col_count = max((cell.column_span for cell in table.body_rows), default=1) if hasattr(table, "body_rows") else 1

        total_rows = (len(table.header_rows) + len(table.body_rows)) if hasattr(table, "header_rows") else len(table.body_rows)

        row_offset = 0
        for header_row in getattr(table, "header_rows", []):
            for cell in header_row.cells:
                cell_text = _text_from_layout(cell.layout, full_text)
                bbox = _bbox_from_layout(cell.layout)
                cells.append(
                    TableCell(
                        row_index=row_offset,
                        column_index=cell.col_span if hasattr(cell, "col_span") else 0,
                        text=cell_text,
                        bounding_box=bbox,
                    )
                )
            row_offset += 1

        for body_row in table.body_rows:
            for cell in body_row.cells:
                cell_text = _text_from_layout(cell.layout, full_text)
                bbox = _bbox_from_layout(cell.layout)
                cells.append(
                    TableCell(
                        row_index=row_offset,
                        column_index=cell.col_span if hasattr(cell, "col_span") else 0,
                        text=cell_text,
                        bounding_box=bbox,
                    )
                )
            row_offset += 1

        bbox = _bbox_from_layout(table.layout)
        tables.append(
            TableStructure(
                row_count=total_rows,
                column_count=col_count,
                cells=cells,
                bounding_box=bbox,
            )
        )
    return tables


def _text_from_layout(
    layout: Any,
    full_text: str,
) -> str:
    """Extract text from a layout element via its text_anchor."""
    if layout and layout.text_anchor:
        return _text_from_text_anchor(layout.text_anchor, full_text)
    return ""


def _text_from_text_anchor(
    text_anchor: Any,
    full_text: str,
) -> str:
    """Extract text from a text_anchor object using segment offsets."""
    if text_anchor and text_anchor.text_segments:
        start = int(text_anchor.text_segments[0].start_index)
        end = int(text_anchor.text_segments[-1].end_index)
        return full_text[start:end].strip()
    return ""


def _bbox_from_layout(layout: Any) -> Optional[BoundingBox]:
    """Build a BoundingBox from a layout element's bounding polygon."""
    if layout and layout.bounding_poly:
        vertices = layout.bounding_poly.normalized_vertices
        if vertices:
            return BoundingBox.from_docai_vertices(
                [{"x": v.x, "y": v.y} for v in vertices]
            )
    return None
