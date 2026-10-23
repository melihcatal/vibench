from typing import Dict, List, Any, Optional, TypedDict
from dataclasses import dataclass


@dataclass
class TextBlock:
    """Represents a block of text with bounding box."""

    text: str
    confidence: float
    geometry: Dict[str, Any]
    block_type: str = "LINE"


@dataclass
class TableCell:
    """Represents a cell in a table."""

    text: str
    row_index: int
    column_index: int
    row_span: int = 1
    column_span: int = 1
    confidence: float = 0.0


@dataclass
class Table:
    """Represents a table structure."""

    cells: List[TableCell]
    row_count: int
    column_count: int
    confidence: float = 0.0


@dataclass
class KeyValuePair:
    """Represents a key-value pair from a form."""

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


class TextractResponseParser:
    """Parser for Textract API responses."""

    @staticmethod
    def parse_text_blocks(response: Dict[str, Any]) -> List[TextBlock]:
        """Extract text blocks from Textract response."""
        blocks = []
        for block in response.get("Blocks", []):
            if block.get("BlockType") == "LINE":
                text_block = TextBlock(
                    text=block.get("Text", ""),
                    confidence=block.get("Confidence", 0.0),
                    geometry=block.get("Geometry", {}),
                    block_type="LINE",
                )
                blocks.append(text_block)
        return blocks

    @staticmethod
    def parse_tables(response: Dict[str, Any]) -> List[Table]:
        """Extract tables from Textract response."""
        tables = []
        blocks = response.get("Blocks", [])

        # Find table blocks
        table_blocks = [b for b in blocks if b.get("BlockType") == "TABLE"]

        for table_block in table_blocks:
            cells = []
            relationships = table_block.get("Relationships", [])

            # Get cell blocks
            cell_ids = []
            for rel in relationships:
                if rel.get("Type") == "CHILD":
                    cell_ids.extend(rel.get("Ids", []))

            # Parse each cell
            for cell_id in cell_ids:
                cell_block = next((b for b in blocks if b.get("Id") == cell_id), None)
                if cell_block:
                    # Get cell text from child relationships
                    cell_text = ""
                    for rel in cell_block.get("Relationships", []):
                        if rel.get("Type") == "CHILD":
                            word_ids = rel.get("Ids", [])
                            words = [
                                b
                                for b in blocks
                                if b.get("Id") in word_ids
                                and b.get("BlockType") == "WORD"
                            ]
                            cell_text = " ".join([w.get("Text", "") for w in words])

                    cell = TableCell(
                        text=cell_text,
                        row_index=cell_block.get("RowIndex", 0),
                        column_index=cell_block.get("ColumnIndex", 0),
                        row_span=cell_block.get("RowSpan", 1),
                        column_span=cell_block.get("ColumnSpan", 1),
                        confidence=cell_block.get("Confidence", 0.0),
                    )
                    cells.append(cell)

            # Determine table dimensions
            if cells:
                row_count = max(cell.row_index for cell in cells)
                column_count = max(cell.column_index for cell in cells)
                table = Table(
                    cells=cells,
                    row_count=row_count,
                    column_count=column_count,
                    confidence=table_block.get("Confidence", 0.0),
                )
                tables.append(table)

        return tables

    @staticmethod
    def parse_key_value_pairs(response: Dict[str, Any]) -> List[KeyValuePair]:
        """Extract key-value pairs from Textract response."""
        pairs = []
        blocks = response.get("Blocks", [])

        # Find key-value set blocks
        kv_blocks = [b for b in blocks if b.get("BlockType") == "KEY_VALUE_SET"]

        for kv_block in kv_blocks:
            entity_type = kv_block.get("EntityTypes", [])
            if "KEY" in entity_type or "VALUE" in entity_type:
                # Get text from child relationships
                text = ""
                for rel in kv_block.get("Relationships", []):
                    if rel.get("Type") == "CHILD":
                        word_ids = rel.get("Ids", [])
                        words = [
                            b
                            for b in blocks
                            if b.get("Id") in word_ids and b.get("BlockType") == "WORD"
                        ]
                        text = " ".join([w.get("Text", "") for w in words])

                # This is simplified - actual key-value pairing requires relationship mapping
                # For now, treat each as separate
                if text:
                    pair = KeyValuePair(
                        key=text if "KEY" in entity_type else "",
                        value=text if "VALUE" in entity_type else "",
                        key_confidence=kv_block.get("Confidence", 0.0)
                        if "KEY" in entity_type
                        else 0.0,
                        value_confidence=kv_block.get("Confidence", 0.0)
                        if "VALUE" in entity_type
                        else 0.0,
                    )
                    pairs.append(pair)

        return pairs
