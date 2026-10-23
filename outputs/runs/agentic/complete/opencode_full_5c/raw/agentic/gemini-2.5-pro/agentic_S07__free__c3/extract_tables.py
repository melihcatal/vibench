from typing import List

from document_client import get_azure_document_intelligence_client
from document_models import Table, TableRow, TableCell


def extract_tables_from_document(document_path: str) -> List[Table]:
    """
    Extracts tables from a document using Azure Document Intelligence.
    """
    document_intelligence_client = get_azure_document_intelligence_client()

    with open(document_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout", document=f
        )
    result = poller.result()

    extracted_tables: List[Table] = []

    if result.tables:
        for table_idx, table in enumerate(result.tables):
            new_table = Table(
                row_count=table.row_count,
                column_count=table.column_count,
                confidence=table.confidence,
                polygon=[
                    p
                    for point in table.bounding_regions[0].polygon
                    for p in (point.x, point.y)
                ],
            )

            rows_map = {}
            for cell in table.cells:
                if cell.row_index not in rows_map:
                    rows_map[cell.row_index] = []

                table_cell = TableCell(
                    content=cell.content,
                    row_index=cell.row_index,
                    column_index=cell.column_index,
                    row_span=cell.row_span if cell.row_span else 1,
                    column_span=cell.column_span if cell.column_span else 1,
                    confidence=cell.confidence,
                    polygon=[
                        p
                        for point in cell.bounding_regions[0].polygon
                        for p in (point.x, point.y)
                    ],
                )
                rows_map[cell.row_index].append(table_cell)

            for row_index in sorted(rows_map.keys()):
                new_row = TableRow(
                    cells=sorted(rows_map[row_index], key=lambda c: c.column_index)
                )
                new_table.rows.append(new_row)

            extracted_tables.append(new_table)

    return extracted_tables
