from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    bucket: str
    key: str
    mime_type: Optional[str] = None
    feature_types: List[str] = field(default_factory=list)
    aws_region: Optional[str] = None


@dataclass
class DocumentLine:
    text: str
    confidence: float = 0.0
    page: int = 1


@dataclass
class DocumentBlock:
    block_type: str
    text: str
    page: int = 1
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentTableCell:
    row_index: int
    column_index: int
    text: str
    confidence: float = 0.0


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: float = 0.0


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    return " ".join(str(text).split())


def normalize_lines(lines: List[Any]) -> List[DocumentLine]:
    normalized = []
    for line in lines:
        if isinstance(line, DocumentLine):
            normalized.append(line)
        elif isinstance(line, dict):
            normalized.append(DocumentLine(text=normalize_text(line.get("text")), confidence=float(line.get("confidence", 0.0)), page=int(line.get("page", 1))))
        else:
            normalized.append(DocumentLine(text=normalize_text(line)))
    return normalized


def normalize_pairs(pairs: List[Any]) -> List[KeyValuePair]:
    normalized = []
    for pair in pairs:
        if isinstance(pair, KeyValuePair):
            normalized.append(pair)
        elif isinstance(pair, dict):
            normalized.append(KeyValuePair(key=normalize_text(pair.get("key")), value=normalize_text(pair.get("value")), confidence=float(pair.get("confidence", 0.0))))
    return normalized
