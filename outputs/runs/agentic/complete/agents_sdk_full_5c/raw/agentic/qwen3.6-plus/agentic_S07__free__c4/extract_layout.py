"""
extract_layout.py - Extracts blocks, lines, tables, and layout elements
from a document using Azure Document Intelligence (Layout model).

Provider: Azure AI Document Intelligence
Model: prebuilt-layout
"""

from typing import Optional, Dict, Any, Union

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.formrecognizer._models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

from document_client import (
    DocumentClientConfig,
    get_azure_doc_intelligence_client,
    normalize_image_to_bytes,
)
from document_models import LayoutResult, LayoutBlock, BoundingBox


def extract_layout_from_document(
    document_data: Union[str, bytes, Any],
    client: Optional[DocumentAnalysisClient] = None,
) -> LayoutResult:
    """
    Extract layout elements (paragraphs, headings, lists, tables)
    from a document image or PDF using Azure Document Intelligence.

    Args:
        document_data: Document as bytes, file path string, or file-like object.
        client: Optional pre-configured DocumentAnalysisClient instance.

    Returns:
        LayoutResult with detected blocks, tables, and page dimensions.
    """
    if client is None:
        client = get_azure_doc_intelligence_client()

    doc_bytes = normalize_image_to_bytes(document_data)

    try:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            document=doc_bytes,
        )
        result: AnalyzeResult = poller.result()
    except HttpResponseError as e:
        raise RuntimeError(f"Azure Document Intelligence layout analysis failed: {e}") from e

    blocks = []
    tables = []

    # Extract paragraphs and other layout elements
    for paragraph in result.paragraphs:
        content = paragraph.content if paragraph.content else ""
        role = paragraph.role if hasattr(paragraph, "role") else None

        # Determine the kind of block based on role or content
        kind = _determine_block_kind(role, content)

        bbox = None
        if hasattr(paragraph, "bounding_regions") and paragraph.bounding_regions:
            region = paragraph.bounding_regions[0]
            polygon = list(region.polygon) if hasattr(region, "polygon") and region.polygon else []
            if len(polygon) >= 8:
                bbox = BoundingBox.from_polygon(polygon).to_dict()

        spans = []
        if hasattr(paragraph, "spans") and paragraph.spans:
            for span in paragraph.spans:
                spans.append({
                    "offset": span.offset if hasattr(span, "offset") else 0,
                    "length": span.length if hasattr(span, "length") else 0,
                })

        blocks.append(LayoutBlock(
            content=content,
            kind=kind,
            bounding_box=bbox,
            spans=spans,
        ))

    # Extract table structures
    for table in result.tables:
        table_data = {
            "row_count": table.row_count if hasattr(table, "row_count") else 0,
            "column_count": table.column_count if hasattr(table, "column_count") else 0,
            "cells": [],
        }

        for cell in table.cells:
            cell_data = {
                "content": cell.content if hasattr(cell, "content") else "",
                "row_index": cell.row_index if hasattr(cell, "row_index") else 0,
                "column_index": cell.column_index if hasattr(cell, "column_index") else 0,
                "row_span": cell.row_span if hasattr(cell, "row_span") else 1,
                "column_span": cell.column_span if hasattr(cell, "column_span") else 1,
                "is_header": cell.kind == "columnHeader" if hasattr(cell, "kind") else False,
            }
            table_data["cells"].append(cell_data)

        tables.append(table_data)

    # Page dimensions
    page_dimensions = None
    if hasattr(result, "pages") and result.pages:
        page = result.pages[0]
        page_dimensions = {
            "width": page.width if hasattr(page, "width") else 0,
            "height": page.height if hasattr(page, "height") else 0,
            "unit": page.unit if hasattr(page, "unit") else "pixel",
        }

    model_id = result.model_id if hasattr(result, "model_id") else "prebuilt-layout"

    return LayoutResult(
        blocks=blocks,
        tables=tables,
        page_dimensions=page_dimensions,
        model_id=model_id,
    )


def _determine_block_kind(role: Optional[str], content: str) -> str:
    """Determine the kind of layout block from Azure DI role metadata."""
    if role == "title":
        return "heading"
    elif role == "pageHeader":
        return "header"
    elif role == "pageFooter":
        return "footer"
    elif role == "footnote":
        return "footnote"
    elif content.startswith(("- ", "* ", "• ")):
        return "listItem"
    elif content.endswith(":"):
        return "sectionHeading"
    return "paragraph"


def extract_layout_from_url(
    document_url: str,
    client: Optional[DocumentAnalysisClient] = None,
) -> LayoutResult:
    """
    Extract layout from a document accessible via URL.

    Args:
        document_url: Public URL of the document.
        client: Optional pre-configured DocumentAnalysisClient instance.

    Returns:
        LayoutResult with detected layout elements.
    """
    if client is None:
        client = get_azure_doc_intelligence_client()

    try:
        poller = client.begin_analyze_document_from_url(
            "prebuilt-layout",
            document_url=document_url,
        )
        result: AnalyzeResult = poller.result()
    except HttpResponseError as e:
        raise RuntimeError(f"Azure Document Intelligence URL layout analysis failed: {e}") from e

    return _parse_azure_layout_result(result)


def _parse_azure_layout_result(result: AnalyzeResult) -> LayoutResult:
    """Parse an Azure AnalyzeResult into a LayoutResult."""
    blocks = []
    tables = []

    for paragraph in result.paragraphs:
        content = paragraph.content if paragraph.content else ""
        role = paragraph.role if hasattr(paragraph, "role") else None
        kind = _determine_block_kind(role, content)

        bbox = None
        if hasattr(paragraph, "bounding_regions") and paragraph.bounding_regions:
            region = paragraph.bounding_regions[0]
            polygon = list(region.polygon) if hasattr(region, "polygon") and region.polygon else []
            if len(polygon) >= 8:
                bbox = BoundingBox.from_polygon(polygon).to_dict()

        blocks.append(LayoutBlock(content=content, kind=kind, bounding_box=bbox))

    for table in result.tables:
        table_data = {
            "row_count": table.row_count if hasattr(table, "row_count") else 0,
            "column_count": table.column_count if hasattr(table, "column_count") else 0,
            "cells": [],
        }
        for cell in table.cells:
            table_data["cells"].append({
                "content": cell.content if hasattr(cell, "content") else "",
                "row_index": cell.row_index if hasattr(cell, "row_index") else 0,
                "column_index": cell.column_index if hasattr(cell, "column_index") else 0,
            })
        tables.append(table_data)

    page_dimensions = None
    if hasattr(result, "pages") and result.pages:
        page = result.pages[0]
        page_dimensions = {
            "width": page.width if hasattr(page, "width") else 0,
            "height": page.height if hasattr(page, "height") else 0,
            "unit": page.unit if hasattr(page, "unit") else "pixel",
        }

    return LayoutResult(
        blocks=blocks,
        tables=tables,
        page_dimensions=page_dimensions,
        model_id="prebuilt-layout",
    )
