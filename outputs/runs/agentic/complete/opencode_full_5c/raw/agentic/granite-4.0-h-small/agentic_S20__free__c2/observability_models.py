from dataclasses import dataclass, asdict
from typing import Any, Dict
import json


@dataclass
class LogEvent:
    """Base log entry model."""

    timestamp: str  # ISO8601 string
    level: str  # DEBUG, INFO, WARNING, ERROR, etc.
    service: str  # originating service name
    message: str  # log payload
    correlation_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class NormalizedLog(LogEvent):
    """Normalized representation for query/response handling."""

    # No extra fields; reuse LogEvent fields, but exposed via helper methods
    pass


@dataclass
class TranslateRequest:
    """Payload for translation API."""

    text: str
    to: str  # target locale code, e.g., 'fr'

    def to_json(self) -> str:
        return json.dumps(asdict(self))


@dataclass
class EmbeddingResponseItem:
    """Individual embedding result from provider API."""

    index: int
    embedding: list[float]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Any:
        return cls(index=d.get("index"), embedding=d.get("embedding"))


@dataclass
class EmbeddingResponse:
    items: list[EmbeddingResponseItem]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Any:
        items = [EmbeddingResponseItem.from_dict(it) for it in d.get("data", [])]
        return cls(items=items)
