from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TextExtractionRequest:
    image_path: str
    mime_type: str = "image/png"


@dataclass
class LayoutExtractionRequest:
    image_path: str
    mime_type: str = "image/png"


@dataclass
class TableExtractionRequest:
    image_path: str
    mime_type: str = "image/png"


@dataclass
class KeyValueExtractionRequest:
    image_path: str
    mime_type: str = "image/png"


def text_from_document(document: Any) -> str:
    return getattr(document, "text", "") or ""


def normalize_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


def blocks_from_document(document: Any) -> List[Dict[str, Any]]:
    blocks: List[Dict[str, Any]] = []
    for page in getattr(document, "pages", []):
        for block in getattr(page, "blocks", []):
            layout = getattr(block, "layout", None)
            blocks.append(
                {
                    "text": layout.text_anchor.content
                    if hasattr(layout, "text_anchor")
                    and hasattr(layout.text_anchor, "content")
                    else "",
                    "confidence": getattr(layout, "confidence", None),
                }
            )
    return blocks


def lines_from_document(document: Any) -> List[Dict[str, Any]]:
    lines: List[Dict[str, Any]] = []
    for page in getattr(document, "pages", []):
        for line in getattr(page, "lines", []):
            layout = getattr(line, "layout", None)
            lines.append(
                {
                    "text": layout.text_anchor.content
                    if hasattr(layout, "text_anchor")
                    and hasattr(layout.text_anchor, "content")
                    else "",
                    "confidence": getattr(layout, "confidence", None),
                }
            )
    return lines


def tables_from_document(document: Any) -> List[Dict[str, Any]]:
    tables: List[Dict[str, Any]] = []
    for page in getattr(document, "pages", []):
        for table in getattr(page, "tables", []):
            tables.append(
                {
                    "header_rows": len(getattr(table, "header_rows", [])),
                    "body_rows": len(getattr(table, "body_rows", [])),
                }
            )
    return tables


def key_values_from_document(document: Any) -> List[Dict[str, Optional[str]]]:
    pairs: List[Dict[str, Optional[str]]] = []
    for entity in getattr(document, "entities", []):
        pairs.append(
            {
                "type": getattr(entity, "type_", None),
                "mention_text": getattr(entity, "mention_text", None),
                "confidence": str(getattr(entity, "confidence", None))
                if getattr(entity, "confidence", None) is not None
                else None,
            }
        )
    return pairs
