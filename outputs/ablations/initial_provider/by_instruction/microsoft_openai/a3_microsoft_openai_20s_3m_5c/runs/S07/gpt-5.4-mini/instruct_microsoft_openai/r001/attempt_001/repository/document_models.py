from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    document_url: str
    model_id: str
    features: Optional[str] = None


@dataclass
class DocumentResponse:
    content: str = ""
    fields: Dict[str, Any] = field(default_factory=dict)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    paragraphs: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_document_response(payload: Dict[str, Any]) -> DocumentResponse:
    analyze_result = payload.get("analyzeResult", payload)
    return DocumentResponse(
        content=analyze_result.get("content", ""),
        fields=analyze_result.get("documents", [{}])[0].get("fields", {}) if analyze_result.get("documents") else {},
        tables=analyze_result.get("tables", []),
        paragraphs=analyze_result.get("paragraphs", []),
        raw=payload,
    )
