from typing import List, Dict, Any


def parse_text(blocks: List[Dict[str, Any]]) -> str:
    lines = [block for block in blocks if block["BlockType"] == "LINE"]
    return "\n".join(block["Text"] for block in lines)


def parse_layout(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    layout = []
    for block in blocks:
        if block["BlockType"] in ["LINE", "WORD", "PARAGRAPH", "TITLE"]:
            layout.append(
                {
                    "type": block["BlockType"],
                    "text": block["Text"],
                    "confidence": block.get("Confidence", 0.0),
                    "geometry": block["Geometry"],
                }
            )
    return layout


def parse_tables(blocks: List[Dict[str, Any]]) -> List[List[List[Dict[str, Any]]]]:
    tables = []
    table_blocks = [b for b in blocks if b["BlockType"] == "TABLE"]
    for table_block in table_blocks:
        cell_map = {}
        if "Relationships" in table_block:
            for relationship in table_block["Relationships"]:
                if relationship["Type"] == "CHILD":
                    for child_id in relationship["Ids"]:
                        cell = next((b for b in blocks if b["Id"] == child_id), None)
                        if cell and cell["BlockType"] == "CELL":
                            row_idx = cell["RowIndex"]
                            column_idx = cell["ColumnIndex"]
                            cell_map[(row_idx, column_idx)] = {
                                "text": cell["Text"],
                                "confidence": cell.get("Confidence", 0.0),
                                "geometry": cell["Geometry"],
                            }
        if cell_map:
            rows = max(row for row, _ in cell_map) + 1
            cols = max(col for _, col in cell_map) + 1
            table = [
                [
                    cell_map.get(
                        (r + 1, c + 1), {"text": "", "confidence": 0.0, "geometry": {}}
                    )
                    for c in range(cols)
                ]
                for r in range(rows)
            ]
            tables.append(table)
    return tables


def parse_key_values(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    key_map: Dict[str, str] = {}
    value_map: Dict[str, str] = {}
    block_map: Dict[str, Dict[str, Any]] = {b["Id"]: b for b in blocks}
    for block in blocks:
        if block["BlockType"] in ["KEY", "VALUE"]:
            text_block_id = None
            for rel in block.get("Relationships", []):
                if rel["Type"] == "CHILD":
                    if rel["Ids"]:
                        text_block_id = rel["Ids"][0]
                    break
            if text_block_id:
                text_block = block_map.get(text_block_id)
                if text_block:
                    text = text_block["Text"]
                    if block["BlockType"] == "KEY":
                        key_map[block["Id"]] = text
                    else:
                        value_map[block["Id"]] = text
    kv_pairs = []
    for block_id, key_text in key_map.items():
        key_block = block_map.get(block_id)
        if key_block:
            for rel in key_block.get("Relationships", []):
                if rel["Type"] == "VALUE":
                    for value_id in rel["Ids"]:
                        value_text = value_map.get(value_id)
                        if value_text:
                            kv_pairs.append(
                                {
                                    "key": key_text,
                                    "value": value_text,
                                    "confidence": key_block.get("Confidence", 0.0),
                                }
                            )
                            break
    return kv_pairs
