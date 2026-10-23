from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Word:
    text: str
    confidence: float = 0.0


@dataclass
class Line:
    text: str
    words: List[Word] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class Block:
    block_type: str
    text: str = ""
    confidence: float = 0.0
    page: int = 1
    row_index: Optional[int] = None
    column_index: Optional[int] = None
    cells: List[List[str]] = field(default_factory=list)
    key: Optional[str] = None
    value: Optional[str] = None


@dataclass
class OcrResult:
    text: str
    lines: List[Line] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutResult:
    blocks: List[Block] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableExtractionResult:
    tables: List[List[List[str]]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_layout(cls, layout: LayoutResult) -> "TableExtractionResult":
        tables: List[List[List[str]]] = []
        for block in layout.blocks:
            if block.block_type == "TABLE" and block.cells:
                tables.append(block.cells)
        return cls(tables=tables, raw=layout.raw)


@dataclass
class KeyValueExtractionResult:
    pairs: Dict[str, str] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_layout(cls, layout: LayoutResult) -> "KeyValueExtractionResult":
        pairs: Dict[str, str] = {}
        for block in layout.blocks:
            if block.block_type == "KEY_VALUE" and block.key is not None:
                pairs[block.key] = block.value or ""
        return cls(pairs=pairs, raw=layout.raw)


def _to_lines_from_blocks(blocks: List[Dict[str, Any]]) -> List[Line]:
    lines: List[Line] = []
    for block in blocks:
        if block.get("BlockType") == "LINE":
            lines.append(Line(text=block.get("Text", ""), confidence=float(block.get("Confidence", 0.0))))
    return lines


def parse_textract_detect_document_text_response(payload: Dict[str, Any]) -> OcrResult:
    blocks = payload.get("Blocks", [])
    lines = _to_lines_from_blocks(blocks)
    text = "\n".join(line.text for line in lines if line.text)
    return OcrResult(text=text, lines=lines, raw=payload)


def parse_textract_analyze_document_response(payload: Dict[str, Any]) -> LayoutResult:
    layout_blocks: List[Block] = []
    for block in payload.get("Blocks", []):
        block_type = block.get("BlockType", "UNKNOWN")
        if block_type == "TABLE":
            cells: List[List[str]] = []
            for rel in block.get("Relationships", []):
                if rel.get("Type") == "CHILD":
                    cells.append([str(rel.get("Ids", []))])
            layout_blocks.append(Block(block_type="TABLE", cells=cells, confidence=float(block.get("Confidence", 0.0)), page=int(block.get("Page", 1))))
        elif block_type == "KEY_VALUE_SET":
            layout_blocks.append(Block(block_type="KEY_VALUE", key=block.get("Text"), value=block.get("Value"), confidence=float(block.get("Confidence", 0.0)), page=int(block.get("Page", 1))))
        else:
            layout_blocks.append(Block(block_type=block_type, text=block.get("Text", ""), confidence=float(block.get("Confidence", 0.0)), page=int(block.get("Page", 1))))
    return LayoutResult(blocks=layout_blocks, raw=payload)
