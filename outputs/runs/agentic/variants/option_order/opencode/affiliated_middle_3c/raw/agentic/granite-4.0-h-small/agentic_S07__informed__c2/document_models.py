# document_models.py
# LOCAL HELPER file
# Defines request/response models and normalization helpers for OCR/layout steps

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class OCRResult:
    """Normalized OCR output model."""

    text: str
    confidence: float | None = None


@dataclass
class LayoutElement:
    """Layout element extracted from Document AI."""

    type: str  # e.g., 'TOKEN', 'BLOCK', 'LINE', 'TABLE'
    text: str | None = None
    bbox: List[float] | None = None  # [x1, y1, x2, y2]


@dataclass
class TableData:
    """Extracted table structure."""

    rows: List[List[Dict[str, Any]]]  # List of rows, each row is list of cell dicts


@dataclass
class KeyValueResult:
    """Key‑Value pair extraction model."""

    key: str
    value: str
    confidence: float | None = None


@dataclass
class TranslationResult:
    """Translation output model."""

    translated_text: str
    source_lang: str | None = None
    target_lang: str | None = None


@dataclass
class SafetyCheckResult:
    """Content safety check output."""

    safe: bool
    flagged: List[str] | None = None  # List of flagged categories (if any)


@dataclass
class FieldExtractionResult:
    """Structured field extraction from OCR‑normalized text."""

    field_name: str
    value: str
    confidence: float | None = None


@dataclass
class EmbeddingResult:
    """Embedding for a document segment."""

    embedding: List[float]
    segment_id: str | None = None
