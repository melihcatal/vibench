from __future__ import annotations

from typing import List

from document_client import get_azure_document_client
from document_models import (
    DocumentInput,
    TableCell,
    TableResult,
    normalize_bbox,
    normalize_text,
)


def extract_tables(document: DocumentInput) -> List[TableResult]:
    client = get_azure_document_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=document.source_bytes,
        content_type=document.mime_type,
    )
    result = poller.result()
    tables: List[TableResult] = []
    for table in result.tables or []:
        cells: List[TableCell] = []
        for cell in table.cells or []:
            cells.append(
                TableCell(
                    row_index=cell.row_index,
                    column_index=cell.column_index,
                    text=normalize_text(getattr(cell, "content", "")),
                    row_span=getattr(cell, "row_span", 1) or 1,
                    column_span=getattr(cell, "column_span", 1) or 1,
                    bbox=normalize_bbox(
                        cell.bounding_regions[0].polygon
                        if cell.bounding_regions
                        else None
                    ),
                )
            )
        page_number = (
            table.bounding_regions[0].page_number if table.bounding_regions else 1
        )
        tables.append(
            TableResult(
                provider="azure-document-intelligence",
                page=page_number,
                cells=cells,
                row_count=getattr(table, "row_count", 0),
                column_count=getattr(table, "column_count", 0),
                raw=table.as_dict() if hasattr(table, "as_dict") else {},
            )
        )
    return tables
