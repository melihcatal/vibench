from document_client import get_client, open_document
from document_models import TableCell, normalize_text


def extract_tables(source: str):
    client = get_client()
    doc = open_document(source)
    if hasattr(doc, "read"):
        poller = client.begin_analyze_document("prebuilt-layout", doc)
    else:
        poller = client.begin_analyze_document_from_url("prebuilt-layout", doc)
    result = poller.result()
    tables = []
    for table in getattr(result, "tables", []) or []:
        cells = []
        for cell in getattr(table, "cells", []) or []:
            cells.append(
                TableCell(
                    row_index=getattr(cell, "row_index", 0),
                    column_index=getattr(cell, "column_index", 0),
                    text=normalize_text(getattr(cell, "content", "")),
                    row_span=getattr(cell, "row_span", 1),
                    column_span=getattr(cell, "column_span", 1),
                    raw=cell,
                )
            )
        tables.append(
            {
                "row_count": getattr(table, "row_count", 0),
                "column_count": getattr(table, "column_count", 0),
                "cells": cells,
                "raw": table,
            }
        )
    return tables
