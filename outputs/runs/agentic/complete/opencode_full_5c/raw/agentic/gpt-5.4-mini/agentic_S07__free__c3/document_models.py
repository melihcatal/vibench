from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    image_source: Any
    language_hints: Optional[List[str]] = None


@dataclass
class DocumentResponse:
    text: str
    raw: Dict[str, Any]


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def to_blocks(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
    pages = raw.get("pages", [])
    blocks = []
    for page in pages:
        for block in page.get("blocks", []):
            blocks.append(block)
    return blocks


def to_tables(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
    pages = raw.get("pages", [])
    tables = []
    for page in pages:
        for block in page.get("blocks", []):
            for paragraph in block.get("paragraphs", []):
                for word in paragraph.get("words", []):
                    for symbol in word.get("symbols", []):
                        _ = symbol
        if "tables" in page:
            tables.extend(page["tables"])
    return tables
