import dataclasses
from typing import Optional, Any


@dataclasses.dataclass
class Secret:
    name: str
    value: Optional[str] = None
    version_id: Optional[str] = None
    arn: Optional[str] = None
    created_date: Optional[Any] = None


@dataclasses.dataclass
class ContentSafetyResult:
    is_safe: bool
    reason: Optional[str] = None


@dataclasses.dataclass
class EmbeddingResult:
    embedding: list[float]


@dataclasses.dataclass
class TranslationResult:
    translated_text: str
