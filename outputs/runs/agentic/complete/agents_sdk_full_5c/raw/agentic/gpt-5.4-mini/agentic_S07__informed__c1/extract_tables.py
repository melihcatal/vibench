from __future__ import annotations

from typing import List, Optional

from document_client import load_document_input, textract_bytes_payload, textract_client
from document_models import TableCell, TableResult


def extract_tables(image_path: Optional[str] = None, content: Optional[bytes] = None, mime_type: str = "image/png") -> List[TableResult]:
    document = load_document_input(content=content, path=image_path, mime_type=mime_type)
    client = textract_client()
    response = client.analyze_document(Document=textract_bytes_payload(document), FeatureTypes=["TABLES"])
    blocks = response.get("Blocks", [])
    block_map = {block.get("Id"): block for block in blocks if block.get("Id")}
    tables: List[TableResult] = []
    for block in blocks:
        if block.get("BlockType") != "TABLE":
            continue
        cells: List[TableCell] = []
        for rel in block.get("Relationships", []):
            if rel.get("Type") != "CHILD":
                continue
            for child_id in rel.get("Ids", []):
                cell = block_map.get(child_id)
                if cell and cell.get("BlockType") == "CELL":
                    cells.append(
                        TableCell(
                            row_index=int(cell.get("RowIndex", 0)),
                            column_index=int(cell.get("ColumnIndex", 0)),
                            text=cell.get("Text", ""),
                            row_span=int(cell.get("RowSpan", 1)),
                            column_span=int(cell.get("ColumnSpan", 1)),
                            raw=cell,
                        )
                    )
        row_count = max((c.row_index + c.row_span - 1 for c in cells), default=0)
        column_count = max((c.column_index + c.column_span - 1 for c in cells), default=0)
        tables.append(TableResult(cells=cells, row_count=row_count, column_count=column_count, raw=block))
    return tables
