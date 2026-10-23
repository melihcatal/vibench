from document_client import get_document_analysis_client, load_image_bytes
from document_models import TableResult, normalize_table_response


AZURE_TABLE_MODEL_ID = "prebuilt-layout"


def extract_tables_from_image(image_path: str) -> TableResult:
    client = get_document_analysis_client()
    image_bytes = load_image_bytes(image_path)
    poller = client.begin_analyze_document(
        model_id=AZURE_TABLE_MODEL_ID, document=image_bytes
    )
    result = poller.result()
    return normalize_table_response(result)


def extract_tables_from_bytes(image_bytes: bytes) -> TableResult:
    client = get_document_analysis_client()
    poller = client.begin_analyze_document(
        model_id=AZURE_TABLE_MODEL_ID, document=image_bytes
    )
    result = poller.result()
    return normalize_table_response(result)


def get_table_csv(table_result: TableResult, table_index: int = 0) -> str:
    return table_result.get_table_as_csv(table_index)


def get_all_tables_csv(table_result: TableResult) -> list:
    csv_outputs = []
    for idx in range(table_result.table_count):
        csv_outputs.append(table_result.get_table_as_csv(idx))
    return csv_outputs


def get_table_dimensions(table_result: TableResult, table_index: int = 0) -> dict:
    if not table_result.tables or table_index >= len(table_result.tables):
        return {"rows": 0, "columns": 0}
    rows = table_result.tables[table_index]
    if not rows:
        return {"rows": 0, "columns": 0}
    num_rows = len(rows)
    num_cols = max(len(row.cells) for row in rows)
    return {"rows": num_rows, "columns": num_cols}
