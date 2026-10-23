
import os
from document_client import get_document_intelligence_client
from document_models import ExtractedLayout

def extract_layout_from_document(document_url: str) -> ExtractedLayout:
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-layout", document_url
    )
    result = poller.result()

    paragraphs = []
    for paragraph in result.paragraphs:
        paragraphs.append({
            "content": paragraph.content,
            "bounding_regions": [{"page_number": region.page_number, "bounding_box": [p.x, p.y for p in region.bounding_regions[0].polygon]} for region in paragraph.bounding_regions] if paragraph.bounding_regions else []
        })

    tables = []
    for table in result.tables:
        cells_data = []
        for cell in table.cells:
            cells_data.append({
                "content": cell.content,
                "row_index": cell.row_index,
                "column_index": cell.column_index,
                "row_span": cell.row_span,
                "column_span": cell.column_span,
            })
        tables.append({
            "rows": table.row_count,
            "columns": table.column_count,
            "cells": cells_data,
        })

    key_values = [] # Layout model does not directly provide key-value pairs, but we keep the structure consistent.

    return ExtractedLayout(paragraphs=paragraphs, tables=tables, key_values=key_values)
