from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from typing import List, Dict, Any
import os

from document_client import get_document_intelligence_client
from document_models import TableResponse


def extract_tables_from_image(image_path: str) -> List[TableResponse]:
    client = get_document_intelligence_client()

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read())
        )

    result = poller.result()

    tables = []
    for table in result.tables:
        rows = {}
        for cell in table.cells:
            if cell.row_index not in rows:
                rows[cell.row_index] = {}
            rows[cell.row_index][cell.column_index] = cell.content

        table_data = []
        for row_index in sorted(rows.keys()):
            row_data = rows[row_index]
            table_data.append([row_data.get(col_index, "") for col_index in sorted(row_data.keys())])

        tables.append(
            TableResponse(
                row_count=table.row_count,
                column_count=table.column_count,
                cells=table_data,
                bounding_box=table.bounding_regions[0].polygon if table.bounding_regions else None
            )
        )

    return tables