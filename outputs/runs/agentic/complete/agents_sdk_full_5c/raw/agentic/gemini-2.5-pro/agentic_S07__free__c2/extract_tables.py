
from typing import List, Union
from document_client import get_document_client
from document_models import ExtractedTable, TableCell

def extract_tables_from_document(file_source: Union[bytes, str]) -> List[ExtractedTable]:
    """
    Extracts tables from a document image or URL using Azure AI Document Intelligence.

    Args:
        file_source: A byte string containing the document content, or a URL string.
    """
    client = get_document_client()

    poller_args = {}
    if isinstance(file_source, bytes):
        poller_args["analyze_request"] = file_source
        poller_args["content_type"] = "application/octet-stream"
    elif isinstance(file_source, str):
        poller_args["url_source"] = file_source
    else:
        raise TypeError("file_source must be bytes or a URL string.")

    poller = client.begin_analyze_document(
        "prebuilt-layout",
        **poller_args
    )
    result = poller.result()

    extracted_tables = []
    if result.tables:
        for table in result.tables:
            cells = []
            for cell in table.cells:
                cells.append(
                    TableCell(
                        content=cell.content,
                        row_index=cell.row_index,
                        column_index=cell.column_index,
                        kind=cell.kind,
                    )
                )
            bounding_box = [
                (point.x, point.y) for point in table.bounding_regions[0].polygon
            ] if table.bounding_regions else []
            
            extracted_tables.append(
                ExtractedTable(
                    cells=cells,
                    row_count=table.row_count,
                    column_count=table.column_count,
                    bounding_box=bounding_box
                )
            )

    return extracted_tables
