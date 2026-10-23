import dataclasses
from typing import Any, Dict, List, Optional


@dataclasses.dataclass
class ModelRequest:
    prompt: str


@dataclasses.dataclass
class ModelResponse:
    text: str
    metadata: Optional[Dict[str, Any]] = None


@dataclasses.dataclass
class SafetyCheckResult:
    attribute_scores: Dict[str, Any]


@dataclasses.dataclass
class TranslationResult:
    translated_text: str
    detected_source_language: str


@dataclasses.dataclass
class EmbeddingResult:
    embedding: List[float]
