import os
from typing import List, Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError
from document_models import (
    TableExtractionRequest,
    Table,
    TableCell,
    TableExtractionResponse,
)


def extract_tables(
    image_path: str, mime_type: Optional[str] = None
) -> TableExtractionResponse:
    """
    Extract table cells and row structure from a document using Amazon Textract.
    """
    textract_client = boto3.client(
        "textract",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = textract_client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
    )

    tables = []
    blocks = response.get("Blocks", [])

    table_blocks = [block for block in blocks if block["BlockType"] == "TABLE"]

    for table_block in table_blocks:
        table_id = table_block["Id"]
        cells = []

        relationships = table_block.get("Relationships", [])
        for relationship in relationships:
            if relationship["Type"] == "CHILD":
                for cell_id in relationship["Ids"]:
                    cell_block = next((b for b in blocks if b["Id"] == cell_id), None)
                    if cell_block and cell_block["BlockType"] == "CELL":
                        row_index = cell_block.get("RowIndex", 0)
                        column_index = cell_block.get("ColumnIndex", 0)
                        row_span = cell_block.get("RowSpan", 1)
                        column_span = cell_block.get("ColumnSpan", 1)

                        cell_text = ""
                        cell_relationships = cell_block.get("Relationships", [])
                        for cell_rel in cell_relationships:
                            if cell_rel["Type"] == "CHILD":
                                for word_id in cell_rel["Ids"]:
                                    word_block = next(
                                        (b for b in blocks if b["Id"] == word_id), None
                                    )
                                    if word_block and word_block["BlockType"] == "WORD":
                                        cell_text += word_block["Text"] + " "

                        cell = TableCell(
                            text=cell_text.strip(),
                            row_index=row_index,
                            column_index=column_index,
                            row_span=row_span,
                            column_span=column_span,
                            confidence=cell_block.get("Confidence", 0.0),
                        )
                        cells.append(cell)

        table = Table(
            cells=cells,
            confidence=table_block.get("Confidence", 0.0),
            bounding_box=table_block.get("Geometry", {}).get("BoundingBox", {}),
        )
        tables.append(table)

    return TableExtractionResponse(
        tables=tables, raw_response=response, provider="amazon_textract"
    )
