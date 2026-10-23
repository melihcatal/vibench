from document_client import get_document_intelligence_client
from document_models import DocumentExtractionResult


def extract_tables_from_document(
    document_content: bytes, mime_type: str
) -> DocumentExtractionResult:
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-layout", document_content, content_type=mime_type
    )
    result = poller.result()

    extracted_tables = []
    for table in result.tables:
        table_data = {
            "row_count": table.row_count,
            "column_count": table.column_count,
            "bounding_box": [p.as_dict() for p in table.polygon],
            "cells": [],
        }
        for cell in table.cells:
            table_data["cells"].append(
                {
                    "content": cell.content,
                    "row_index": cell.row_index,
                    "column_index": cell.column_index,
                    "row_span": cell.row_span,
                    "column_span": cell.column_span,
                    "bounding_box": [p.as_dict() for p in cell.polygon],
                }
            )
        extracted_tables.append(table_data)

    return DocumentExtractionResult(tables=extracted_tables)
