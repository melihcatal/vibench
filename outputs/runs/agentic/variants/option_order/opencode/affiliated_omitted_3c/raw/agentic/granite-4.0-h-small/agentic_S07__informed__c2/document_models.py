import json
from typing import Any, Dict, List, Tuple


def normalize_text(doc: Dict[str, Any]) -> str:
    """
    Convert Document AI response to plain text string.

    Args:
        doc: Document node from API response.
    Returns:
        Full extracted text in reading order.
    """
    lines = []
    for page in doc.pages:
        for block in page.blocks:
            # Layout blocks that are text
            if block.type == 5:  # TEXT
                for paragraph in block.layout.paragraphs:
                    for token in paragraph.tokens:
                        lines.append(token.text)
    return " ".join(lines)


def layout_elements(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Convert layout structure into a list of dictionaries describing blocks, lines,
    and tables.
    """
    result = []
    for page in doc.pages:
        for block in page.blocks:
            block_data = {
                "id": block.id,
                "type": block.type,
                "boundingPoly": block.layout.boundingPoly.vertices,
                "text": " ".join(
                    token.text for token in block.layout.paragraphs[0].tokens
                ),
            }
            result.append(block_data)
    return result


def tables_structure(doc: Dict[str, Any]) -> List[List[List[str]]]:
    """
    Extract tables as a list of rows, each row a list of cell values.

    This is a simplified extraction; real tables may need more logic.
    """
    tables = []
    for page in doc.pages:
        for table in page.tables:
            rows = []
            for row in table.rows:
                cells = [cell.layout.content for cell in row.cells]
                rows.append(cells)
            tables.append(rows)
    return tables


def key_value_mapping(doc: Dict[str, Any]) -> Dict[str, str]:
    """
    Extract key-value pairs from a form layout.

    Finds entities marked as KEY and VALUE and pairs them by proximity.
    """
    keys = []
    values = []
    for block in doc.blocks:
        if block.type == 9:  # KEY
            keys.append(
                (
                    block.layout.boundingPoly.vertices,
                    block.layout.paragraphs[0].tokens[0].text,
                )
            )
        if block.type == 10:  # VALUE
            values.append(
                (
                    block.layout.boundingPoly.vertices,
                    block.layout.paragraphs[0].tokens[0].text,
                )
            )
    # Simple heuristic: pair each key with the nearest value
    kv = {}
    for key_bbox, key_text in keys:
        nearest = None
        nearest_dist = float("inf")
        for value_bbox, value_text in values:
            # approximate distance using bounding box centroids
            key_center = (
                (key_bbox[0].x + key_bbox[2].x) / 2,
                (key_bbox[0].y + key_bbox[2].y) / 2,
            )
            value_center = (
                (value_bbox[0].x + value_bbox[2].x) / 2,
                (value_bbox[0].y + value_bbox[2].y) / 2,
            )
            dist = (
                (key_center[0] - value_center[0]) ** 2
                + (key_center[1] - value_center[1]) ** 2
            ) ** 0.5
            if dist < nearest_dist:
                nearest_dist = dist
                nearest = value_text
        if nearest is not None:
            kv[key_text] = nearest
    return kv


def normalize_processed_document(doc: Dict[str, Any]) -> str:
    """Unified normalization that returns plain text."""
    return normalize_text(doc)
