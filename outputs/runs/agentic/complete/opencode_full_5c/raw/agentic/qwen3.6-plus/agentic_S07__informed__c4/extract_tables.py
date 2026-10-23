from document_client import process_document
from document_models import build_ocr_result, OcrResult, TableData, TableCell


def extract_tables_from_image(
    file_bytes: bytes, mime_type: str = "image/png"
) -> OcrResult:
    document = process_document(file_bytes, mime_type=mime_type)
    result = build_ocr_result(document)
    return result


def extract_tables_from_file(file_path: str, mime_type: str = "image/png") -> OcrResult:
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    return extract_tables_from_image(file_bytes, mime_type=mime_type)


def get_tables(result: OcrResult) -> list:
    return result.tables


def get_table_cells(table: TableData) -> list:
    return table.cells


def get_table_as_rows(table: TableData) -> list:
    rows = {}
    for cell in table.cells:
        if cell.row_index not in rows:
            rows[cell.row_index] = []
        while len(rows[cell.row_index]) < cell.col_index + cell.col_span:
            rows[cell.row_index].append("")
        for ci in range(cell.col_span):
            rows[cell.row_index][cell.col_index + ci] = cell.text
    return [rows[i] for i in sorted(rows.keys())]
