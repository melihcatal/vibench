import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from document_client import get_azure_document_intelligence_client
from document_models import ExtractedTable, TableCell, BoundingRegion

def extract_document_tables(document_content: bytes) -> list[ExtractedTable]:
    client = get_azure_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-layout", document_content
    )
    result = poller.result()

    extracted_tables = []
    for table in result.tables:
        cells = []
        for cell in table.cells:
            cells.append(TableCell(
                content=cell.content,
                row_index=cell.row_index,
                column_index=cell.column_index,
                row_span=cell.row_span if cell.row_span else 1,
                column_span=cell.column_span if cell.column_span else 1,
                kind=cell.kind
            ))
        
        extracted_tables.append(ExtractedTable(
            row_count=table.row_count,
            column_count=table.column_count,
            cells=cells,
            bounding_regions=[BoundingRegion(
                page_number=region.page_number,
                polygon=list(region.polygon)
            ) for region in table.bounding_regions]
        ))

    return extracted_tables
