from typing import List
from document_client import get_document_intelligence_client
from document_models import Table


def extract_tables_from_document(file_path: str) -> List[Table]:
    """
    Extracts tables from a document.
    """
    document_intelligence_client = get_document_intelligence_client()

    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    extracted_tables = []
    if result.tables:
        for table_idx, table in enumerate(result.tables):
            cells = [
                ["" for _ in range(table.column_count)] for _ in range(table.row_count)
            ]
            for cell in table.cells:
                cells[cell.row_index][cell.column_index] = cell.content

            bounding_box = []
            if table.bounding_regions:
                for region in table.bounding_regions:
                    bounding_box.extend([(p.x, p.y) for p in region.polygon])

            extracted_tables.append(
                Table(
                    cells=cells,
                    row_count=table.row_count,
                    column_count=table.column_count,
                    bounding_box=bounding_box,
                )
            )
    return extracted_tables
