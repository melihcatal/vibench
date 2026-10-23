from typing import TypedDict, List, Literal
from datetime import datetime


class LogEvent(TypedDict):
    timestamp: int  # epoch milliseconds
    message: str
    severity: str
    request_id: str | None
    correlation_id: str | None


class SafetyCheckResult(TypedDict):
    flagged: bool
    severity: float  # 0.0 - 1.0
    attribute: str


class TranslationResult(TypedDict):
    source: str
    target: str
    translated_text: str


class EmbeddingResult(TypedDict):
    model: str
    embeddings: List[dict]
