import io
from document_client import get_document_intelligence_client

def extract_tables(payload):
    client = get_document_intelligence_client()
    with client:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            body=io.BytesIO(payload['document_bytes']), 
            content_type=payload['mime_type']
        )
        result = poller.result()

    tables = []
    for table in result.tables:
        cells_data = []
        for cell in table.cells:
            cells_data.append({
                "content": cell.content,
                "row_index": cell.row_index,
                "column_index": cell.column_index,
                "row_span": cell.row_span or 1,
                "column_span": cell.column_span or 1,
            })
        tables.append({
            "row_count": table.row_count,
            "column_count": table.column_count,
            "cells": cells_data
        })
    return {"tables": tables}
