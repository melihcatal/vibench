from typing import Optional

from document_client import (
    get_textract_client,
    build_textract_image_bytes,
    normalize_textract_response,
)
from document_models import TableResponse, normalize_table_response


TEXTRACT_MODEL_ID = "aws:textract:tables"


def extract_tables_from_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> TableResponse:
    client = get_textract_client()
    image_doc = build_textract_image_bytes(
        image_path=image_path, image_bytes=image_bytes
    )
    response = client.analyze_document(
        Document=image_doc,
        FeatureTypes=["TABLES"],
    )
    normalized = normalize_textract_response(response)
    result = normalize_table_response(normalized)
    return result


def extract_tables_with_layout(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> TableResponse:
    client = get_textract_client()
    image_doc = build_textract_image_bytes(
        image_path=image_path, image_bytes=image_bytes
    )
    response = client.analyze_document(
        Document=image_doc,
        FeatureTypes=["TABLES", "LAYOUT"],
    )
    normalized = normalize_textract_response(response)
    result = normalize_table_response(normalized)
    return result


def extract_tables_from_s3(
    bucket: str,
    key: str,
    version: Optional[str] = None,
) -> TableResponse:
    client = get_textract_client()
    s3_object = {"Bucket": bucket, "Name": key}
    if version:
        s3_object["Version"] = version
    response = client.analyze_document(
        Document={"S3Object": s3_object},
        FeatureTypes=["TABLES"],
    )
    normalized = normalize_textract_response(response)
    result = normalize_table_response(normalized)
    return result


def get_table_cells_as_grid(table_response: TableResponse) -> list:
    grids = []
    for table in table_response.tables:
        grid = [["" for _ in range(table.column_count)] for _ in range(table.row_count)]
        for cell in table.cells:
            if (
                0 < cell.row_index <= table.row_count
                and 0 < cell.column_index <= table.column_count
            ):
                grid[cell.row_index - 1][cell.column_index - 1] = cell.text
        grids.append(grid)
    return grids
