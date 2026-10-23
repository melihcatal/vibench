import os
from typing import List, Optional
from document_client import get_document_client
from document_models import TableExtractionResponse, Table, TableCell


def extract_tables(image_path: str, mime_type: Optional[str] = None) -> TableExtractionResponse:
    """
    Extract tables and their cell structures from a document using Azure AI Document Intelligence.
    """
    client = get_document_client()

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        analyze_request=image_data,
        content_type="application/octet-stream"
    )
    result = poller.result()

    tables = []
    for table in result.tables:
        cells = []
        for cell in table.cells:
            cells.append(TableCell(
                row_index=cell.row_index,
                column_index=cell.column_index,
                text=cell.content,
                bounding_box=cell.bounding_regions[0].polygon if cell.bounding_regions else None
            ))
        tables.append(Table(
            rows=table.row_count,
            columns=table.column_count,
            cells=cells
        ))

    return TableExtractionResponse(tables=tables)