import boto3
from document_client import load_image_bytes
from document_models import TablesResult
from typing import List


def extract_tables(image_path: str) -> TablesResult:
    client = boto3.client("textract", region_name="us-east-1")
    content = load_image_bytes(image_path)
    response = client.analyze_document(
        Document={"Bytes": content}, FeatureTypes=["TABLES"]
    )
    blocks = response["Blocks"]
    tables = []
    table_blocks = [b for b in blocks if b["BlockType"] == "TABLE"]
    for table_block in table_blocks:
        cells = [
            b
            for b in blocks
            if b["BlockType"] == "CELL"
            and any(
                rel["Id"] == table_block["Id"] for rel in b.get("Relationships", [])
            )
        ]
        if not cells:
            continue
        max_row = max(int(c["RowIndex"]) + int(c.get("RowSpan", 1)) for c in cells)
        max_col = max(
            int(c["ColumnIndex"]) + int(c.get("ColumnSpan", 1)) for c in cells
        )
        grid: List[List[str]] = [["" for _ in range(max_col)] for _ in range(max_row)]
        for cell in cells:
            row = int(cell["RowIndex"])
            col = int(cell["ColumnIndex"])
            rowspan = int(cell.get("RowSpan", 1))
            colspan = int(cell.get("ColumnSpan", 1))
            text = cell["Text"]
            for r in range(row, row + rowspan):
                for c in range(col, col + colspan):
                    grid[r][c] = text
        tables.append(grid)
    return {"tables": tables}
