from document_client import get_document_intelligence_client
from document_models import ExtractedLayoutResult, DocumentProcessingRequest
import io

def extract_layout_elements(request: DocumentProcessingRequest) -> ExtractedLayoutResult:
    """
    Extracts blocks, lines, tables, or layout elements from a document using Azure Document Intelligence.
    """
    client = get_document_intelligence_client()

    if request.document_url:
        poller = client.begin_analyze_document(
            "prebuilt-layout", document_url=request.document_url
        )
    elif request.document_content and request.content_type:
        document_stream = io.BytesIO(request.document_content)
        poller = client.begin_analyze_document(
            "prebuilt-layout", document_stream, content_type=request.content_type
        )
    else:
        raise ValueError("Either document_url or document_content and content_type must be provided.")

    result = poller.result()

    # Simplistic representation of layout for the purpose of this example
    pages_layout = []
    if result.pages:
        for page in result.pages:
            tables_on_page = []
            if result.tables:
                for table in result.tables:
                    # Filter tables belonging to the current page
                    if table.bounding_regions and any(region.page_number == page.page_number for region in table.bounding_regions):
                        tables_on_page.append({
                            "row_count": table.row_count,
                            "column_count": table.column_count,
                            "cells": [{"content": cell.content, "row_index": cell.row_index, "column_index": cell.column_index} for cell in table.cells]
                        })

            lines_on_page = []
            if page.lines:
                lines_on_page = [{"content": line.content, "bounding_box": line.polygon} for line in page.lines]

            pages_layout.append({
                "page_number": page.page_number,
                "width": page.width,
                "height": page.height,
                "unit": page.unit,
                "lines": lines_on_page,
                "tables": tables_on_page,
                "words": [{"content": word.content, "bounding_box": word.polygon} for word in page.words] if page.words else []
            })
    return ExtractedLayoutResult(pages=pages_layout)
