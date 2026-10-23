"""Local request, response, and normalization helpers for structured document extraction."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


@dataclass
class StructuredDocumentRequest:
    document_bytes: Optional[bytes] = None
    bucket: Optional[str] = None
    key: Optional[str] = None
    content_type: Optional[str] = None


@dataclass
class StructuredField:
    value: Any
    confidence: Optional[float] = None
    label: Optional[str] = None


@dataclass
class StructuredDocumentResponse:
    fields: Dict[str, StructuredField] = field(default_factory=dict)
    raw: Optional[Dict[str, Any]] = None


def normalize_confidence(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        score = float(value)
    except (TypeError, ValueError):
        return None
    return max(0.0, min(1.0, score / 100.0 if score > 1 else score))


def normalize_currency_amount(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip().replace(",", "")
    return text or None


def merge_field_maps(*maps: Mapping[str, StructuredField]) -> Dict[str, StructuredField]:
    merged: Dict[str, StructuredField] = {}
    for mp in maps:
        merged.update(mp)
    return merged
