import io
from document_client import get_document_intelligence_client

def extract_layout(payload):
    client = get_document_intelligence_client()
    with client:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            body=io.BytesIO(payload['document_bytes']), 
            content_type=payload['mime_type']
        )
        result = poller.result()

    layout_elements = {
        "paragraphs": [{
            "content": p.content,
            "bounding_regions": [{"page_number": br.page_number, "polygon": br.polygon} for br in p.bounding_regions]
        } for p in result.paragraphs],
        "tables": [{
            "row_count": t.row_count,
            "column_count": t.column_count,
            "cells": [{
                "content": c.content,
                "row_index": c.row_index,
                "column_index": c.column_index,
                "row_span": c.row_span,
                "column_span": c.column_span,
                "bounding_regions": [{"page_number": br.page_number, "polygon": br.polygon} for br in c.bounding_regions]
            } for c in t.cells]
        } for t in result.tables],
        "figures": [{
            "bounding_regions": [{"page_number": br.page_number, "polygon": br.polygon} for br in f.bounding_regions]
        } for f in result.figures],
    }
    return layout_elements
