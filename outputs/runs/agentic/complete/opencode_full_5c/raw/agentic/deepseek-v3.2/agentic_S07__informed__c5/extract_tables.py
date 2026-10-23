import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_client import get_document_client
from document_models import Table, TableCell, BoundingBox


def extract_tables_from_image(image_path: str) -> list[Table]:
    """Extract table cells and row structure from a document using Azure Document Intelligence."""
    client = get_document_client()

    with open(image_path, "rb") as f:
        image_data = f.read()

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=image_data,
        content_type="application/octet-stream",
    )

    result = poller.result()

    tables = []

    if hasattr(result, "tables"):
        for table in result.tables:
            cells = []
            for cell in table.cells:
                table_cell = TableCell(
                    row_index=cell.row_index,
                    column_index=cell.column_index,
                    row_span=cell.row_span,
                    column_span=cell.column_span,
                    content=cell.content,
                    bounding_box=BoundingBox(
                        x=cell.bounding_regions[0].polygon[0].x
                        if cell.bounding_regions
                        else 0,
                        y=cell.bounding_regions[0].polygon[0].y
                        if cell.bounding_regions
                        else 0,
                        width=cell.bounding_regions[0].polygon[2].x
                        - cell.bounding_regions[0].polygon[0].x
                        if cell.bounding_regions
                        and len(cell.bounding_regions[0].polygon) >= 3
                        else 0,
                        height=cell.bounding_regions[0].polygon[2].y
                        - cell.bounding_regions[0].polygon[0].y
                        if cell.bounding_regions
                        and len(cell.bounding_regions[0].polygon) >= 3
                        else 0,
                    ),
                )
                cells.append(table_cell)

            table_obj = Table(
                rows=table.row_count,
                columns=table.column_count,
                cells=cells,
                bounding_box=BoundingBox(
                    x=table.bounding_regions[0].polygon[0].x
                    if table.bounding_regions
                    else 0,
                    y=table.bounding_regions[0].polygon[0].y
                    if table.bounding_regions
                    else 0,
                    width=table.bounding_regions[0].polygon[2].x
                    - table.bounding_regions[0].polygon[0].x
                    if table.bounding_regions
                    and len(table.bounding_regions[0].polygon) >= 3
                    else 0,
                    height=table.bounding_regions[0].polygon[2].y
                    - table.bounding_regions[0].polygon[0].y
                    if table.bounding_regions
                    and len(table.bounding_regions[0].polygon) >= 3
                    else 0,
                ),
            )
            tables.append(table_obj)

    return tables


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python extract_tables.py <image_path>")
        sys.exit(1)

    tables = extract_tables_from_image(sys.argv[1])
    for i, table in enumerate(tables):
        print(f"Table {i + 1}: {table.rows}x{table.columns}")
        for cell in table.cells:
            print(f"  Cell [{cell.row_index},{cell.column_index}]: {cell.content}")
