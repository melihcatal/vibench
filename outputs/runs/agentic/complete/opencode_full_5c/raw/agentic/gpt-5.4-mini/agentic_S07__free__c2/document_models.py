from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    source_url: Optional[str] = None
    source_bytes: Optional[bytes] = None


@dataclass
class NormalizedWord:
    text: str
    confidence: Optional[float] = None


def normalize_document_response(payload: Dict[str, Any]) -> Dict[str, Any]:
    result = payload.get("analyzeResult", payload)
    pages = result.get("pages", [])
    content = result.get("content", "")
    lines = []
    for page in pages:
        lines.extend(page.get("lines", []))
    return {
        "content": content,
        "pages": pages,
        "lines": lines,
        "tables": result.get("tables", []),
        "documents": result.get("documents", []),
    }


def normalize_key_values(documents: List[Dict[str, Any]]) -> Dict[str, str]:
    output: Dict[str, str] = {}
    for doc in documents:
        for field_name, field in doc.get("fields", {}).items():
            value = (
                field.get("content") or field.get("valueString") or field.get("value")
            )
            if value is not None:
                output[field_name] = str(value)
    return output
