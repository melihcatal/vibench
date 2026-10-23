import os
from typing import BinaryIO, List
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_models import TableResponse, TableCell

def extract_tables(image_data: BinaryIO) -> List[TableResponse]:
    """Extract table cells and row structure from a document using Azure Form Recognizer."""
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
    
    if not endpoint or not key:
        raise ValueError("Azure Form Recognizer credentials not configured.")
    
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    poller = client.begin_analyze_document("prebuilt-layout", document=image_data.read())
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
        tables.append(TableResponse(
            row_count=table.row_count,
            column_count=table.column_count,
            cells=cells
        ))
    
    return tables