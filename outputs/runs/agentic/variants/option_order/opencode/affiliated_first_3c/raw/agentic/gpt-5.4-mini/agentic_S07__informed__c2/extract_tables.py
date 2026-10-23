from document_client import get_document_intelligence_client, get_model_id
from document_models import OCRRequest


def extract_tables(image):
    request = OCRRequest(image=image)
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        get_model_id("tables"), document=request.to_bytes()
    )
    result = poller.result()
    tables = []
    for table in getattr(result, "tables", []):
        rows = {}
        for cell in getattr(table, "cells", []):
            rows.setdefault(getattr(cell, "row_index", 0), []).append(
                getattr(cell, "content", "")
            )
        tables.append(
            {
                "row_count": len(rows),
                "cells": getattr(table, "cells", []),
                "rows": [rows[i] for i in sorted(rows)],
            }
        )
    return {"model_id": get_model_id("tables"), "tables": tables, "raw": result}
