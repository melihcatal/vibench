from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class BlockType(Enum):
    PAGE = "PAGE"
    LINE = "LINE"
    WORD = "WORD"
    TABLE = "TABLE"
    CELL = "CELL"
    KEY_VALUE_SET = "KEY_VALUE_SET"
    SELECTION_ELEMENT = "SELECTION_ELEMENT"


@dataclass
class TextBlock:
    """Represents a text block from OCR."""

    text: str
    confidence: float
    geometry: Dict[str, Any]
    block_type: BlockType
    id: str


@dataclass
class TableCell:
    """Represents a table cell."""

    row_index: int
    column_index: int
    text: str
    confidence: float
    geometry: Dict[str, Any]


@dataclass
class Table:
    """Represents a table structure."""

    cells: List[TableCell]
    row_count: int
    column_count: int
    geometry: Dict[str, Any]


@dataclass
class KeyValuePair:
    """Represents a key-value pair."""

    key: str
    value: str
    key_confidence: float
    value_confidence: float


@dataclass
class DocumentAnalysisResult:
    """Container for document analysis results."""

    text_blocks: List[TextBlock]
    tables: List[Table]
    key_value_pairs: List[KeyValuePair]
    raw_response: Dict[str, Any]


def normalize_textract_response(response: Dict[str, Any]) -> DocumentAnalysisResult:
    """Normalize Textract response to common format."""
    blocks = response.get("Blocks", [])

    text_blocks = []
    tables = []
    key_value_pairs = []

    # Map block IDs for relationship resolution
    block_map = {block["Id"]: block for block in blocks}

    # Process blocks
    for block in blocks:
        block_type = BlockType(block.get("BlockType"))

        if block_type in [BlockType.LINE, BlockType.WORD]:
            text_blocks.append(
                TextBlock(
                    text=block.get("Text", ""),
                    confidence=block.get("Confidence", 0.0),
                    geometry=block.get("Geometry", {}),
                    block_type=block_type,
                    id=block["Id"],
                )
            )

        elif block_type == BlockType.TABLE:
            # Extract table cells
            cells = []
            for relationship in block.get("Relationships", []):
                if relationship["Type"] == "CHILD":
                    for cell_id in relationship["Ids"]:
                        cell_block = block_map.get(cell_id)
                        if cell_block and cell_block.get("BlockType") == "CELL":
                            # Find row and column indices
                            row_index = cell_block.get("RowIndex", 0)
                            column_index = cell_block.get("ColumnIndex", 0)

                            # Get cell text from child relationships
                            cell_text = ""
                            for cell_rel in cell_block.get("Relationships", []):
                                if cell_rel["Type"] == "CHILD":
                                    for word_id in cell_rel["Ids"]:
                                        word_block = block_map.get(word_id)
                                        if (
                                            word_block
                                            and word_block.get("BlockType") == "WORD"
                                        ):
                                            cell_text += (
                                                word_block.get("Text", "") + " "
                                            )
                            cell_text = cell_text.strip()

                            cells.append(
                                TableCell(
                                    row_index=row_index,
                                    column_index=column_index,
                                    text=cell_text,
                                    confidence=cell_block.get("Confidence", 0.0),
                                    geometry=cell_block.get("Geometry", {}),
                                )
                            )

            # Determine table dimensions
            row_count = max((cell.row_index for cell in cells), default=0)
            column_count = max((cell.column_index for cell in cells), default=0)

            tables.append(
                Table(
                    cells=cells,
                    row_count=row_count,
                    column_count=column_count,
                    geometry=block.get("Geometry", {}),
                )
            )

        elif block_type == BlockType.KEY_VALUE_SET:
            entity_type = block.get("EntityTypes", [])
            if "KEY" in entity_type or "VALUE" in entity_type:
                # Extract key-value relationships
                key_text = ""
                value_text = ""
                key_conf = 0.0
                value_conf = 0.0

                for relationship in block.get("Relationships", []):
                    if relationship["Type"] == "CHILD":
                        for child_id in relationship["Ids"]:
                            child_block = block_map.get(child_id)
                            if child_block and child_block.get("BlockType") == "WORD":
                                text = child_block.get("Text", "")
                                conf = child_block.get("Confidence", 0.0)
                                if "KEY" in entity_type:
                                    key_text += text + " "
                                    key_conf = max(key_conf, conf)
                                else:
                                    value_text += text + " "
                                    value_conf = max(value_conf, conf)

                key_text = key_text.strip()
                value_text = value_text.strip()

                if key_text and value_text:
                    key_value_pairs.append(
                        KeyValuePair(
                            key=key_text,
                            value=value_text,
                            key_confidence=key_conf,
                            value_confidence=value_conf,
                        )
                    )

    return DocumentAnalysisResult(
        text_blocks=text_blocks,
        tables=tables,
        key_value_pairs=key_value_pairs,
        raw_response=response,
    )
