from typing import List
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from document_client import get_document_client
from document_models import Table, TableCell, BoundingBox, Point

def extract_tables_from_url(document_url: str) -> List[Table]:
    """
    Extracts tables from a document image using Azure AI Document Intelligence.

    Args:
        document_url: The URL of the document to analyze.

    Returns:
        A list of Table objects found in the document.
    """
    client = get_document_client()
    poller = client.begin_analyze_document(
        "prebuilt-layout", AnalyzeDocumentRequest(url_source=document_url)
    )
    result = poller.result()

    extracted_tables = []
    if result.tables:
        for table_idx, table in enumerate(result.tables):
            cells = []
            for cell in table.cells:
                points = [Point(p.x, p.y) for p in cell.bounding_regions[0].polygon]
                bounding_box = BoundingBox(points=(points[0], points[1], points[2], points[3]))
                
                cells.append(TableCell(
                    content=cell.content,
                    row_index=cell.row_index,
                    column_index=cell.column_index,
                    bounding_box=bounding_box,
                    kind=cell.kind or "content"
                ))
            
            table_region = table.bounding_regions[0]
            table_points = [Point(p.x, p.y) for p in table_region.polygon]
            table_bounding_box = BoundingBox(points=(table_points[0], table_points[1], table_points[2], table_points[3]))

            extracted_tables.append(Table(
                cells=cells,
                row_count=table.row_count,
                column_count=table.column_count,
                bounding_box=table_bounding_box,
                page_number=table_region.page_number,
            ))
    return extracted_tables
