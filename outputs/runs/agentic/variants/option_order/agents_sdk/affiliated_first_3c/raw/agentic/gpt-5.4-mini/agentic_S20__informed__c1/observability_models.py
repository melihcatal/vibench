from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _coerce_datetime(value: Any) -> str:
    if value is None:
        return utc_now_iso()
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    return str(value)


def normalize_severity(value: Any) -> str:
    if value is None:
        return "INFO"
    text = str(value).strip().upper()
    aliases = {"WARN": "WARNING", "ERR": "ERROR", "CRIT": "CRITICAL"}
    return aliases.get(text, text)


def normalize_log_event(event: Mapping[str, Any]) -> Dict[str, Any]:
    payload = dict(event)
    payload.setdefault("timestamp", utc_now_iso())
    payload["timestamp"] = _coerce_datetime(payload.get("timestamp"))
    payload["severity"] = normalize_severity(payload.get("severity"))
    if "message" in payload and payload["message"] is not None:
        payload["message"] = str(payload["message"])
    return payload


def build_structured_event(message: str, severity: str = "INFO", **fields: Any) -> Dict[str, Any]:
    event: Dict[str, Any] = {"message": message, "severity": severity, **fields}
    return normalize_log_event(event)


def build_correlation_event(message: str, correlation_id: str, severity: str = "INFO", **fields: Any) -> Dict[str, Any]:
    event = {"message": message, "severity": severity, "correlation_id": correlation_id, **fields}
    return normalize_log_event(event)


@dataclass
class LogIngestResponse:
    provider: str
    status: str
    raw: Any = None
    request_id: Optional[str] = None


@dataclass
class LogQueryResult:
    provider: str
    records: List[Dict[str, Any]] = field(default_factory=list)
    raw: Any = None
    next_token: Optional[str] = None

    def recent_messages(self) -> List[str]:
        return [str(item.get("message", "")) for item in self.records]


@dataclass
class SafetyResult:
    provider: str
    is_safe: bool
    categories: Dict[str, float] = field(default_factory=dict)
    raw: Any = None


@dataclass
class TranslationResult:
    provider: str
    target_language: str
    translated_text: str
    raw: Any = None


@dataclass
class EmbeddingResult:
    provider: str
    vectors: List[List[float]]
    raw: Any = None


@dataclass
class IncidentSummary:
    provider: str
    summary: str
    raw: Any = None
