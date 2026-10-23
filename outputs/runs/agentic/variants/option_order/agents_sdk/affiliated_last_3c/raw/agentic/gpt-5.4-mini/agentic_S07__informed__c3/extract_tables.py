from __future__ import annotations

from collections import defaultdict
from typing import List, Optional

from document_client import get_textract_client
from document_models import TableCell, TableResult


def extract_tables(image_bytes: bytes, mime_type: str = "image/png", region_name: Optional[str] = None) -> List[TableResult]:
    helper = get_textract_client(region_name=region_name)
    response = helper.client.analyze_document(
        Document={"Bytes": image_bytes},
        FeatureTypes=["TABLES"],
    )
    blocks = response.get("Blocks", [])
    block_map = {b.get("Id"): b for b in blocks if b.get("Id")}
    results: List[TableResult] = []
    for block in blocks:
        if block.get("BlockType") != "TABLE":
            continue
        cells: List[TableCell] = []
        rows = defaultdict(dict)
        for rel in block.get("Relationships", []):
            if rel.get("Type") != "CHILD":
                continue
            for child_id in rel.get("Ids", []):
                cell = block_map.get(child_id)
                if not cell or cell.get("BlockType") != "CELL":
                    continue
                text = ""
                for cell_rel in cell.get("Relationships", []):
                    if cell_rel.get("Type") == "CHILD":
                        text = " ".join(block_map.get(wid, {}).get("Text", "") for wid in cell_rel.get("Ids", []))
                row_index = int(cell.get("RowIndex", 0))
                col_index = int(cell.get("ColumnIndex", 0))
                cells.append(TableCell(row_index=row_index, column_index=col_index, text=text, row_span=int(cell.get("RowSpan", 1)), column_span=int(cell.get("ColumnSpan", 1)), confidence=cell.get("Confidence")))
                rows[row_index][col_index] = text
        ordered_rows = [[row.get(col, "") for col in sorted(row)] for _, row in sorted(rows.items())]
        results.append(TableResult(cells=cells, rows=ordered_rows, raw=block))
    return results
