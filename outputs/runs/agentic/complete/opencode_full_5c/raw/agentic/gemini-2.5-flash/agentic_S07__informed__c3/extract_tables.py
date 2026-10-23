from document_client import get_document_intelligence_client
from document_models import ExtractedTables
import io


def extract_tables_from_document(document_content: bytes) -> ExtractedTables:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        "prebuilt-layout", document_content, content_type="application/octet-stream"
    )
    result = poller.result()
    tables_data = []
    if result.tables:
        for table in result.tables:
            cells = []
            for cell in table.cells:
                cells.append(
                    {
                        "content": cell.content,
                        "row_index": cell.row_index,
                        "column_index": cell.column_index,
                        "row_span": cell.row_span,
                        "column_span": cell.column_span,
                    }
                )
            tables_data.append(
                {
                    "bounding_regions": [r.to_dict() for r in table.bounding_regions],
                    "cells": cells,
                    "row_count": table.row_count,
                    "column_count": table.column_count,
                }
            )
    return ExtractedTables(tables=tables_data)
