from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentSource:
    content: bytes
    mime_type: str
    filename: Optional[str] = None


@dataclass
class OCRTextResult:
    provider: str
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class LayoutResult:
    provider: str
    elements: List[Dict[str, Any]]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TableResult:
    provider: str
    tables: List[Dict[str, Any]]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class KeyValueResult:
    provider: str
    pairs: List[Dict[str, Any]]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    detected_language: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class SafetyResult:
    provider: str
    flagged: bool
    categories: Dict[str, Any]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class FieldExtractionResult:
    provider: str
    fields: Dict[str, Any]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    embeddings: List[List[float]]
    raw_response: Optional[Dict[str, Any]] = None


def normalize_polygon(bounding_poly: Dict[str, Any]) -> List[Dict[str, float]]:
    vertices = (
        bounding_poly.get("normalizedVertices") or bounding_poly.get("vertices") or []
    )
    normalized = []
    for vertex in vertices:
        normalized.append(
            {
                "x": float(vertex.get("x", 0.0)),
                "y": float(vertex.get("y", 0.0)),
            }
        )
    return normalized


def normalize_text_anchor(anchor: Dict[str, Any], full_text: str) -> str:
    text_segments = anchor.get("textSegments", [])
    chunks: List[str] = []
    for segment in text_segments:
        start_index = int(segment.get("startIndex", 0) or 0)
        end_index = int(segment.get("endIndex", 0) or 0)
        chunks.append(full_text[start_index:end_index])
    return "".join(chunks).strip()


def compact_whitespace(value: str) -> str:
    return " ".join(value.split())
