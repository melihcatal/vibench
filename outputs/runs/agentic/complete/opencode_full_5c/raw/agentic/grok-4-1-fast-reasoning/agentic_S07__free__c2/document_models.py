from typing import List, Dict, Any

Block = Dict[str, Any]


def normalize_ocr_text(blocks: List[Block]) -> str:
    line_texts = [block["Text"] for block in blocks if block["BlockType"] == "LINE"]
    return "\n".join(line_texts)


def normalize_layout_elements(blocks: List[Block]) -> List[Dict[str, Any]]:
    elements = []
    for block in blocks:
        block_type = block["BlockType"]
        if block_type.startswith("LAYOUT_"):
            geometry = block.get("Geometry", {}).get("BoundingBox", {})
            elements.append(
                {
                    "id": block["Id"],
                    "type": block_type,
                    "text": block.get("Text", ""),
                    "confidence": block.get("Confidence", 0.0),
                    "bounding_box": geometry,
                }
            )
    return elements


def parse_tables(blocks: List[Block]) -> List[List[List[str]]]:
    tables = []
    table_blocks = [b for b in blocks if b["BlockType"] == "TABLE"]
    for table_block in table_blocks:
        cells = []
        for rel in table_block.get("Relationships", []):
            if rel["Type"] == "CHILD":
                child_id = rel["Ids"][0]
                cell_block = next(
                    (
                        b
                        for b in blocks
                        if b["Id"] == child_id and b["BlockType"] == "CELL"
                    ),
                    None,
                )
                if cell_block:
                    cells.append(cell_block)
        if cells:
            rows: Dict[int, List[Dict[str, Any]]] = {}
            for cell in cells:
                row_idx = cell["RowIndex"]
                if row_idx not in rows:
                    rows[row_idx] = []
                rows[row_idx].append(cell)
            table_rows = []
            for row_idx in sorted(rows.keys()):
                row_cells = sorted(rows[row_idx], key=lambda c: c["ColumnIndex"])
                row_texts = [c.get("Text", "") for c in row_cells]
                table_rows.append(row_texts)
            tables.append(table_rows)
    return tables


def extract_key_value_pairs(blocks: List[Block]) -> List[Dict[str, str]]:
    pairs = []
    for block in blocks:
        if (
            block["BlockType"] == "KEY_VALUE_SET"
            and block.get("EntityTypes")
            and block["EntityTypes"][0] == "KEY"
        ):
            for relationship in block.get("Relationships", []):
                if relationship["Type"] == "VALUE":
                    value_id = relationship["Ids"][0]
                    value_block = next((b for b in blocks if b["Id"] == value_id), None)
                    if value_block:
                        pairs.append(
                            {
                                "key": block.get("Text", "").strip(),
                                "value": value_block.get("Text", "").strip(),
                            }
                        )
    return pairs
