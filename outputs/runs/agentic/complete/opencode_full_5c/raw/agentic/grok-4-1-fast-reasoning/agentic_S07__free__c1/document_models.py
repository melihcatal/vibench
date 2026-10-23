from typing import List, Dict, Any, TypedDict


class LayoutElement(TypedDict):
    id: str
    type: str
    text: str
    confidence: float
    bbox: Dict[str, float]
    relationships: List[Dict[str, Any]]


class Table(TypedDict):
    rows: List[List[str]]


def extract_full_text(blocks: List[Dict[str, Any]]) -> str:
    text_parts = []
    for block in blocks:
        if block.get("BlockType") == "LINE" and "Text" in block:
            text_parts.append(block["Text"])
    return "\n".join(text_parts).strip()


def extract_layout_elements(blocks: List[Dict[str, Any]]) -> List[LayoutElement]:
    elements = []
    for block in blocks:
        block_type = block.get("BlockType")
        if block_type != "WORD":
            geom = block.get("Geometry", {})
            bbox = geom.get("BoundingBox", {})
            elements.append(
                {
                    "id": block["Id"],
                    "type": block_type,
                    "text": block.get("Text", ""),
                    "confidence": block.get("Confidence", 0.0),
                    "bbox": bbox,
                    "relationships": block.get("Relationships", []),
                }
            )
    return elements


def extract_tables(blocks: List[Dict[str, Any]]) -> List[List[List[str]]]:
    block_map: Dict[str, Dict[str, Any]] = {
        b["Id"]: b for b in blocks if b.get("BlockType") == "CELL"
    }
    tables = []
    table_blocks = [b for b in blocks if b.get("BlockType") == "TABLE"]
    for table_block in table_blocks:
        child_rels = [
            r for r in table_block.get("Relationships", []) if r["Type"] == "CHILD"
        ]
        child_ids = [cid for rel in child_rels for cid in rel["Ids"]]
        row_indices = set()
        col_indices = set()
        for cell_id in child_ids:
            if cell_id in block_map:
                cell = block_map[cell_id]
                row_indices.add(cell["RowIndex"])
                col_indices.add(cell["ColumnIndex"])
        if row_indices and col_indices:
            max_row = max(row_indices)
            max_col = max(col_indices)
            table: List[List[str]] = [
                ["" for _ in range(max_col)] for _ in range(max_row)
            ]
            for cell_id in child_ids:
                if cell_id in block_map:
                    cell = block_map[cell_id]
                    row = cell["RowIndex"] - 1
                    col = cell["ColumnIndex"] - 1
                    text = cell.get("Text", "")
                    table[row][col] = text
            tables.append(table)
    return tables


def extract_key_value_pairs(blocks: List[Dict[str, Any]]) -> Dict[str, str]:
    block_map: Dict[str, Dict[str, Any]] = {b["Id"]: b for b in blocks}
    kv_pairs = {}
    for block in blocks:
        if block.get("BlockType") == "KEY":
            for rel in block.get("Relationships", []):
                if rel["Type"] == "VALUE":
                    for val_id in rel["Ids"]:
                        val_block = block_map.get(val_id)
                        if val_block and val_block.get("BlockType") == "VALUE":
                            key = block.get("Text", "").strip()
                            value = val_block.get("Text", "").strip()
                            kv_pairs[key] = value
                            break
    return kv_pairs
