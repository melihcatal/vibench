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
class TextractBlock:
    id: str
    block_type: BlockType
    text: Optional[str] = None
    confidence: Optional[float] = None
    geometry: Optional[Dict[str, Any]] = None
    relationships: Optional[List[Dict[str, Any]]] = None
    entity_types: Optional[List[str]] = None

    @classmethod
    def from_aws_response(cls, block_data: Dict[str, Any]) -> "TextractBlock":
        return cls(
            id=block_data.get("Id", ""),
            block_type=BlockType(block_data.get("BlockType", "")),
            text=block_data.get("Text"),
            confidence=block_data.get("Confidence"),
            geometry=block_data.get("Geometry"),
            relationships=block_data.get("Relationships"),
            entity_types=block_data.get("EntityTypes"),
        )


@dataclass
class DocumentTextResult:
    text: str
    blocks: List[TextractBlock]
    raw_response: Dict[str, Any]

    @classmethod
    def from_textract_response(cls, response: Dict[str, Any]) -> "DocumentTextResult":
        blocks = []
        text_parts = []

        for block_data in response.get("Blocks", []):
            block = TextractBlock.from_aws_response(block_data)
            blocks.append(block)
            if block.block_type == BlockType.LINE and block.text:
                text_parts.append(block.text)

        return cls(text="\n".join(text_parts), blocks=blocks, raw_response=response)


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    confidence: float


@dataclass
class TableResult:
    table_id: str
    cells: List[TableCell]
    rows: int
    columns: int

    def to_list_of_lists(self) -> List[List[str]]:
        table = [["" for _ in range(self.columns)] for _ in range(self.rows)]
        for cell in self.cells:
            if (
                0 <= cell.row_index < self.rows
                and 0 <= cell.column_index < self.columns
            ):
                table[cell.row_index][cell.column_index] = cell.text
        return table


@dataclass
class KeyValuePair:
    key: str
    value: str
    key_confidence: float
    value_confidence: float


@dataclass
class KeyValueResult:
    pairs: List[KeyValuePair]

    def to_dict(self) -> Dict[str, str]:
        return {pair.key: pair.value for pair in self.pairs}


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class SafetyCheckResult:
    text: str
    is_safe: bool
    toxicity_score: float
    categories: Dict[str, float]


@dataclass
class FieldExtractionResult:
    fields: Dict[str, Any]
    confidence_scores: Dict[str, float]
    document_type: str


@dataclass
class EmbeddingResult:
    text: str
    embedding: List[float]
    model_id: str
