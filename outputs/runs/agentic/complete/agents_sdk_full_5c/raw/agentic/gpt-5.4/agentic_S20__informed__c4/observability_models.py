from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional
import json
import uuid


SEVERITY_MAP = {
    "debug": "DEBUG",
    "info": "INFO",
    "notice": "INFO",
    "warning": "WARNING",
    "warn": "WARNING",
    "error": "ERROR",
    "critical": "CRITICAL",
    "alert": "ALERT",
    "emergency": "EMERGENCY",
}


@dataclass
class StructuredLogEvent:
    message: str
    service: str
    severity: str = "INFO"
    correlation_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    labels: Dict[str, str] = field(default_factory=dict)
    json_payload: Dict[str, Any] = field(default_factory=dict)

    def normalize(self) -> "StructuredLogEvent":
        severity = SEVERITY_MAP.get(self.severity.lower(), self.severity.upper())
        correlation_id = self.correlation_id or str(uuid.uuid4())
        return StructuredLogEvent(
            message=self.message,
            service=self.service,
            severity=severity,
            correlation_id=correlation_id,
            timestamp=self.timestamp,
            labels=dict(self.labels),
            json_payload=dict(self.json_payload),
        )

    def to_gcp_entry(self) -> Dict[str, Any]:
        event = self.normalize()
        payload = {
            "message": event.message,
            "service": event.service,
            "correlation_id": event.correlation_id,
            **event.json_payload,
        }
        labels = {**event.labels, "service": event.service, "correlation_id": event.correlation_id}
        return {
            "json_payload": payload,
            "severity": event.severity,
            "labels": labels,
            "timestamp": event.timestamp,
        }


@dataclass
class LogQueryRequest:
    service: Optional[str] = None
    severity: Optional[str] = None
    correlation_id: Optional[str] = None
    field_filters: Dict[str, Any] = field(default_factory=dict)
    minutes: int = 15
    limit: int = 50

    def build_filter(self) -> str:
        clauses: List[str] = []
        if self.service:
            clauses.append(f'labels.service="{self.service}"')
        if self.severity:
            sev = SEVERITY_MAP.get(self.severity.lower(), self.severity.upper())
            clauses.append(f'severity={sev}')
        if self.correlation_id:
            clauses.append(f'labels.correlation_id="{self.correlation_id}"')
        for key, value in self.field_filters.items():
            if isinstance(value, str):
                escaped = value.replace('"', '\\"')
                clauses.append(f'jsonPayload.{key}="{escaped}"')
            elif isinstance(value, bool):
                clauses.append(f'jsonPayload.{key}={str(value).lower()}')
            else:
                clauses.append(f'jsonPayload.{key}={json.dumps(value)}')
        return " AND ".join(clauses)


@dataclass
class NormalizedLogEntry:
    timestamp: Optional[str]
    severity: Optional[str]
    message: str
    service: Optional[str]
    correlation_id: Optional[str]
    labels: Dict[str, str] = field(default_factory=dict)
    payload: Dict[str, Any] = field(default_factory=dict)


def normalize_gcp_entries(entries: Iterable[Any]) -> List[NormalizedLogEntry]:
    normalized: List[NormalizedLogEntry] = []
    for entry in entries:
        payload = getattr(entry, "payload", None) or {}
        labels = dict(getattr(entry, "labels", {}) or {})
        if isinstance(payload, str):
            message = payload
            payload_dict: Dict[str, Any] = {"message": payload}
        else:
            payload_dict = dict(payload)
            message = str(payload_dict.get("message", ""))
        normalized.append(
            NormalizedLogEntry(
                timestamp=getattr(entry, "timestamp", None).isoformat() if getattr(entry, "timestamp", None) else None,
                severity=str(getattr(entry, "severity", "")) if getattr(entry, "severity", None) else None,
                message=message,
                service=labels.get("service") or payload_dict.get("service"),
                correlation_id=labels.get("correlation_id") or payload_dict.get("correlation_id"),
                labels=labels,
                payload=payload_dict,
            )
        )
    return normalized
