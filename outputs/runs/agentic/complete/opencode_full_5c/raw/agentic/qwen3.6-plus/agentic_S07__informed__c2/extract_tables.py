import os
from typing import Optional
from alibabacloud_ocr_api20210707.models import RecognizeTableRequest
from document_client import create_ocr_client, encode_image_to_base64
from document_models import DocumentTableResult, TableStructure, TableCell


def extract_tables_from_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> DocumentTableResult:
    client = create_ocr_client()
    image_base64 = encode_image_to_base64(image_path, image_bytes)

    request = RecognizeTableRequest(body=image_base64)
    response = client.recognize_table(request)

    body = response.body
    tables = []

    if hasattr(body, "data") and body.data:
        data = body.data
        if isinstance(data, dict):
            table_list = data.get("tables", [data])
            for table_data in table_list:
                cells = []
                row_indices = set()
                col_indices = set()

                for cell_data in table_data.get("cells", []):
                    row_idx = cell_data.get("row", cell_data.get("row_index", 0))
                    col_idx = cell_data.get("column", cell_data.get("col_index", 0))
                    cell = TableCell(
                        row_index=row_idx,
                        col_index=col_idx,
                        text=cell_data.get("text", ""),
                        confidence=cell_data.get("confidence", 0.0),
                    )
                    cells.append(cell)
                    row_indices.add(row_idx)
                    col_indices.add(col_idx)

                num_rows = table_data.get(
                    "num_rows", max(row_indices) + 1 if row_indices else 0
                )
                num_columns = table_data.get(
                    "num_columns", max(col_indices) + 1 if col_indices else 0
                )

                tables.append(
                    TableStructure(
                        cells=cells,
                        num_rows=num_rows,
                        num_columns=num_columns,
                    )
                )

    return DocumentTableResult(tables=tables, page_count=1)


if __name__ == "__main__":
    image_file = os.environ.get("DOCUMENT_IMAGE_PATH")
    if image_file:
        result = extract_tables_from_image(image_path=image_file)
        for idx, table in enumerate(result.tables):
            print(f"Table {idx}: {table.num_rows} rows x {table.num_columns} columns")
            for cell in table.cells:
                print(f"  [{cell.row_index},{cell.col_index}] {cell.text}")
