from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentImageRequest:
    image_url: Optional[str] = None
    image_path: Optional[str] = None
    content_type: str = "application/octet-stream"


@dataclass
class DocumentTextResponse:
    text: str
    raw: Dict[str, Any]


@dataclass
class DocumentLayoutResponse:
    blocks: List[Dict[str, Any]]
    raw: Dict[str, Any]


@dataclass
class DocumentTableResponse:
    tables: List[Dict[str, Any]]
    raw: Dict[str, Any]


@dataclass
class DocumentKeyValueResponse:
    key_values: List[Dict[str, Any]]
    raw: Dict[str, Any]


def normalize_analyzed_document(payload: Dict[str, Any]) -> Dict[str, Any]:
    result = payload.get("analyzeResult", payload)
    content = result.get("content", "")
    paragraphs = result.get("paragraphs", []) or []
    tables = result.get("tables", []) or []
    key_values = result.get("keyValuePairs", []) or []
    lines = []
    for page in result.get("pages", []) or []:
        for line in page.get("lines", []) or []:
            lines.append(line)
    return {"content": content, "paragraphs": paragraphs, "tables": tables, "keyValuePairs": key_values, "lines": lines, "raw": payload}
