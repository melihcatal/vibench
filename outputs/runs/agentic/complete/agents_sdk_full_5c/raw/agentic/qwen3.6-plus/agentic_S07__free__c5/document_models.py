"""
Document models for OCR and Layout Extraction.

Defines local request, response, and normalization helpers for
OCR and Layout Extraction results from AWS Textract.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple


@dataclass
class TextBlock:
    """Represents a text block extracted from a document."""
    text: str
    confidence: float
    block_type: str
    geometry: Optional[Dict[str, Any]] = None
    page: int = 0
    id: Optional[str] = None


@dataclass
class LayoutElement:
    """Represents a layout element (section, figure, table, etc.)."""
    element_type: str
    text: str
    confidence: float
    bounding_box: Optional[Dict[str, Any]] = None
    page: int = 0
    children: List[str] = field(default_factory=list)
    id: Optional[str] = None


@dataclass
class TableRow:
    """Represents a row in an extracted table."""
    row_index: int
    cells: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0
    page: int = 0


@dataclass
class TableCell:
    """Represents a cell in an extracted table."""
    text: str
    row_index: int
    col_index: int
    row_span: int = 1
    col_span: int = 1
    is_header: bool = False
    confidence: float = 0.0


@dataclass
class ExtractedTable:
    """Represents a complete extracted table."""
    table_id: str
    rows: List[TableRow] = field(default_factory=list)
    page: int = 0
    confidence: float = 0.0


@dataclass
class KeyValue:
    """Represents a key-value pair extracted from a form."""
    key: str
    value: str
    key_confidence: float = 0.0
    value_confidence: float = 0.0
    page: int = 0


@dataclass
class OcrTextResult:
    """Container for plain text OCR results."""
    full_text: str
    pages: int
    blocks: List[TextBlock] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class LayoutResult:
    """Container for layout extraction results."""
    elements: List[LayoutElement] = field(default_factory=list)
    pages: int = 0
    sections: List[str] = field(default_factory=list)


@dataclass
class TableResult:
    """Container for table extraction results."""
    tables: List[ExtractedTable] = field(default_factory=list)
    pages: int = 0


@dataclass
class KeyValueResult:
    """Container for key-value extraction results."""
    pairs: List[KeyValue] = field(default_factory=list)
    pages: int = 0


def normalize_textract_block(block: Dict[str, Any]) -> TextBlock:
    """
    Normalize an AWS Textract block response to TextBlock.
    
    Args:
        block: Raw Textract block dictionary.
        
    Returns:
        TextBlock: Normalized text block.
    """
    return TextBlock(
        text=block.get("Text", ""),
        confidence=block.get("Confidence", 0.0),
        block_type=block.get("BlockType", "UNKNOWN"),
        geometry=block.get("Geometry"),
        page=block.get("Page", 0),
        id=block.get("Id"),
    )


def normalize_textract_blocks(blocks: List[Dict[str, Any]]) -> List[TextBlock]:
    """
    Normalize a list of AWS Textract blocks to TextBlock list.
    
    Args:
        blocks: List of raw Textract block dictionaries.
        
    Returns:
        List[TextBlock]: Normalized text blocks.
    """
    return [normalize_textract_block(b) for b in blocks if b.get("BlockType") in ("LINE", "WORD")]


def normalize_textract_layout_elements(blocks: List[Dict[str, Any]]) -> List[LayoutElement]:
    """
    Normalize Textract blocks to layout elements.
    
    Args:
        blocks: List of raw Textract block dictionaries.
        
    Returns:
        List[LayoutElement]: Normalized layout elements.
    """
    elements = []
    for block in blocks:
        block_type = block.get("BlockType", "")
        if block_type in (
            "LAYOUT_SECTION_HEADER", "LAYOUT_FIGURE", "LAYOUT_TABLE",
            "LAYOUT_LIST", "LAYOUT_TEXT", "LAYOUT_HEADER", "LAYOUT_FOOTER",
            "LAYOUT_PAGE_HEADER", "LAYOUT_PAGE_FOOTER", "LAYOUT_TITLE",
            "LAYOUT_KEY_VALUE", "LAYOUT_KEY", "LAYOUT_VALUE",
        ):
            element_text = block.get("Text", "")
            relations = block.get("Relationships", [])
            child_ids = []
            for rel in relations:
                if rel.get("Type") == "CHILD":
                    child_ids.extend(rel.get("Ids", []))
            
            elements.append(LayoutElement(
                element_type=block_type,
                text=element_text,
                confidence=block.get("Confidence", 0.0),
                bounding_box=block.get("Geometry", {}).get("BoundingBox"),
                page=block.get("Page", 0),
                children=child_ids,
                id=block.get("Id"),
            ))
    return elements


def normalize_textract_table(table_block: Dict[str, Any], all_blocks: List[Dict[str, Any]]) -> ExtractedTable:
    """
    Normalize a Textract table block to ExtractedTable.
    
    Args:
        table_block: Raw Textract table block dictionary.
        all_blocks: All blocks from the Textract response.
        
    Returns:
        ExtractedTable: Normalized table structure.
    """
    cell_blocks = [
        b for b in all_blocks
        if b.get("BlockType") == "CELL" and b.get("Id") in table_block.get("Relationships", [{}])[0].get("Ids", [])
    ]
    
    rows_dict: Dict[int, List[Dict[str, Any]]] = {}
    for cell in cell_blocks:
        row_idx = cell.get("RowIndex", 0)
        col_idx = cell.get("ColumnIndex", 0)
        cell_text = cell.get("Text", "")
        is_header = row_idx == 1
        
        rows_dict.setdefault(row_idx, []).append({
            "col_index": col_idx,
            "text": cell_text,
            "confidence": cell.get("Confidence", 0.0),
            "is_header": is_header,
            "row_span": cell.get("RowSpan", 1),
            "col_span": cell.get("ColumnSpan", 1),
        })
    
    table_rows = []
    for row_idx in sorted(rows_dict.keys()):
        cells = rows_dict[row_idx]
        cells.sort(key=lambda c: c["col_index"])
        row = TableRow(
            row_index=row_idx,
            cells=cells,
            confidence=min(c["confidence"] for c in cells) if cells else 0.0,
            page=table_block.get("Page", 0),
        )
        table_rows.append(row)
    
    return ExtractedTable(
        table_id=table_block.get("Id", ""),
        rows=table_rows,
        page=table_block.get("Page", 0),
        confidence=table_block.get("Confidence", 0.0),
    )


def normalize_textract_key_values(
    key_value_blocks: List[Dict[str, Any]],
    all_blocks: List[Dict[str, Any]],
) -> List[KeyValue]:
    """
    Normalize Textract key-value set blocks to KeyValue pairs.
    
    Args:
        key_value_blocks: List of KEY_VALUE_SET blocks from Textract.
        all_blocks: All blocks from the Textract response.
        
    Returns:
        List[KeyValue]: Normalized key-value pairs.
    """
    block_map = {b["Id"]: b for b in all_blocks}
    pairs = []
    
    for kv_block in key_value_blocks:
        if kv_block.get("EntityTypes") and "KEY" in kv_block.get("EntityTypes", []):
            key_text = kv_block.get("Text", "")
            key_conf = kv_block.get("Confidence", 0.0)
            
            value_text = ""
            value_conf = 0.0
            
            relations = kv_block.get("Relationships", [])
            for rel in relations:
                if rel.get("Type") == "VALUE":
                    for val_id in rel.get("Ids", []):
                        val_block = block_map.get(val_id, {})
                        value_conf = val_block.get("Confidence", 0.0)
                        
                        value_words = []
                        for vrel in val_block.get("Relationships", []):
                            if vrel.get("Type") == "CHILD":
                                for child_id in vrel.get("Ids", []):
                                    child = block_map.get(child_id, {})
                                    if child.get("BlockType") == "WORD":
                                        value_words.append(child.get("Text", ""))
                        value_text = " ".join(value_words)
                        break
            
            pairs.append(KeyValue(
                key=key_text,
                value=value_text,
                key_confidence=key_conf,
                value_confidence=value_conf,
                page=kv_block.get("Page", 0),
            ))
    
    return pairs


def aggregate_text_from_blocks(blocks: List[TextBlock]) -> str:
    """
    Aggregate text from a list of TextBlocks into a single string.
    
    Args:
        blocks: List of TextBlock objects.
        
    Returns:
        str: Combined text with proper spacing.
    """
    lines = []
    current_page = 0
    for block in sorted(blocks, key=lambda b: (b.page, b.id or "")):
        if block.page != current_page and current_page > 0:
            lines.append("")
        if block.block_type == "LINE":
            lines.append(block.text)
        current_page = block.page
    return "\n".join(lines)


def calculate_average_confidence(blocks: List[TextBlock]) -> float:
    """
    Calculate average confidence score from blocks.
    
    Args:
        blocks: List of TextBlock objects.
        
    Returns:
        float: Average confidence score.
    """
    if not blocks:
        return 0.0
    return sum(b.confidence for b in blocks) / len(blocks)
