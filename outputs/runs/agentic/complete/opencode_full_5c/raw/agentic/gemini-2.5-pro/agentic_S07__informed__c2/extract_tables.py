from document_client import get_document_client
from document_models import ExtractedTables, Table, TableCell


def extract_tables_from_document(file_path: str) -> ExtractedTables:
    """
    Extracts table structures from a document.
    """
    document_intelligence_client = get_document_client()

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
            cells = []
            for cell in table.cells:
                cells.append(
                    TableCell(
                        row_index=cell.row_index,
                        column_index=cell.column_index,
                        content=cell.content,
                        kind=cell.kind,
                    )
                )

            bounding_box = []
            if table.bounding_regions:
                for region in table.bounding_regions:
                    bounding_box.extend(region.polygon)

            extracted_tables.append(
                Table(
                    row_count=table.row_count,
                    column_count=table.column_count,
                    cells=cells,
                    bounding_box=bounding_box,
                )
            )

    return ExtractedTables(tables=extracted_tables)
