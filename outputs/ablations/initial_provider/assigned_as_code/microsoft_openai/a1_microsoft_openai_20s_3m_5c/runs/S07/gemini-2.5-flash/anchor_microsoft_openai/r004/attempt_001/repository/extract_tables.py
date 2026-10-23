import io
from document_client import get_document_intelligence_client
from document_models import DocumentAnalysisResponse

def extract_tables(payload):
    client = get_document_intelligence_client()
    with client:
        poller = client.begin_analyze_document(
            "prebuilt-layout", # Using layout model as it also extracts tables
            body=io.BytesIO(payload['document_bytes']), 
            content_type=payload['mime_type']
        )
        result = poller.result()

    tables_data = []
    for table in result.tables:
        cells_data = []
        for cell in table.cells:
            cells_data.append({
                "row_index": cell.row_index,
                "column_index": cell.column_index,
                "content": cell.content,
                "bounding_regions": [br.as_dict() for br in cell.bounding_regions]
            })
        tables_data.append({
            "row_count": table.row_count,
            "column_count": table.column_count,
            "cells": cells_data,
            "bounding_regions": [br.as_dict() for br in table.bounding_regions]
        })

    return DocumentAnalysisResponse(tables=tables_data)._asdict()
