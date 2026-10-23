from document_client import get_azure_document_client, load_image_bytes
from document_models import TableCell, TableResult


def extract_tables_from_image(image_path: str) -> list[TableResult]:
    client = get_azure_document_client()
    image_bytes = load_image_bytes(image_path)
    poller = client.begin_analyze_document(model_id="prebuilt-layout", body=image_bytes)
    result = poller.result()
    table_results = []
    for table in result.tables or []:
        cells = []
        for cell in table.cells:
            cells.append(
                TableCell(
                    content=cell.content or "",
                    row_index=cell.row_index,
                    col_index=cell.column_index,
                    row_span=cell.row_span or 1,
                    col_span=cell.column_span or 1,
                )
            )
        table_results.append(
            TableResult(
                cells=cells, row_count=table.row_count, col_count=table.column_count
            )
        )
    return table_results
