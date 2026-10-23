from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping, Sequence


GOOGLE_AUDIT_PROVIDER = "google"
GOOGLE_AUDIT_API_HOST = "https://www.googleapis.com"


def _normalize_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _normalize_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    return _normalize_str(value).lower() in {"1", "true", "t", "yes", "y", "on"}


def _normalize_timestamp(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    text = _normalize_str(value)
    if not text:
        return datetime.now(timezone.utc)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _normalize_mapping(data: Mapping[str, Any]) -> dict[str, Any]:
    return {str(key): value for key, value in data.items()}


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    provider: str = GOOGLE_AUDIT_PROVIDER
    subject: str = ""
    email: str = ""
    success: bool = True
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    client_id: str = ""
    ip_address: str = ""
    user_agent: str = ""
    error_code: str = ""
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AuditEvent":
        mapping = _normalize_mapping(data)
        return cls(
            event_type=_normalize_str(mapping.get("event_type") or mapping.get("event") or mapping.get("action")),
            provider=_normalize_str(mapping.get("provider")) or GOOGLE_AUDIT_PROVIDER,
            subject=_normalize_str(mapping.get("subject") or mapping.get("sub") or mapping.get("user_id")),
            email=_normalize_str(mapping.get("email")).lower(),
            success=_normalize_bool(mapping.get("success", True)),
            timestamp=_normalize_timestamp(mapping.get("timestamp") or mapping.get("time") or mapping.get("created_at")),
            client_id=_normalize_str(mapping.get("client_id") or mapping.get("audience")),
            ip_address=_normalize_str(mapping.get("ip_address") or mapping.get("ip")),
            user_agent=_normalize_str(mapping.get("user_agent") or mapping.get("ua")),
            error_code=_normalize_str(mapping.get("error_code") or mapping.get("error")),
            raw=dict(mapping),
        )


@dataclass(frozen=True)
class AuditSummary:
    provider: str
    total_events: int
    success_count: int
    failure_count: int
    event_counts: dict[str, int]
    unique_subjects: int
    unique_emails: int
    top_clients: list[tuple[str, int]]
    top_errors: list[tuple[str, int]]
    first_event_at: datetime | None
    last_event_at: datetime | None


def summarize_audit_events(events: Sequence[Mapping[str, Any] | AuditEvent], provider: str = GOOGLE_AUDIT_PROVIDER, top_n: int = 5) -> AuditSummary:
    normalized_events = [event if isinstance(event, AuditEvent) else AuditEvent.from_mapping(event) for event in events]
    filtered = [event for event in normalized_events if event.provider == provider]
    total_events = len(filtered)
    success_count = sum(1 for event in filtered if event.success)
    failure_count = total_events - success_count
    event_counts = Counter(event.event_type or "unknown" for event in filtered)
    subjects = {event.subject for event in filtered if event.subject}
    emails = {event.email for event in filtered if event.email}
    client_counts = Counter(event.client_id for event in filtered if event.client_id)
    error_counts = Counter(event.error_code for event in filtered if event.error_code)
    timestamps = sorted((event.timestamp for event in filtered), default=None)
    first_event_at = timestamps[0] if timestamps else None
    last_event_at = timestamps[-1] if timestamps else None
    return AuditSummary(
        provider=provider,
        total_events=total_events,
        success_count=success_count,
        failure_count=failure_count,
        event_counts=dict(event_counts),
        unique_subjects=len(subjects),
        unique_emails=len(emails),
        top_clients=client_counts.most_common(top_n),
        top_errors=error_counts.most_common(top_n),
        first_event_at=first_event_at,
        last_event_at=last_event_at,
    )


def summarize_audit_events_by_day(events: Iterable[Mapping[str, Any] | AuditEvent], provider: str = GOOGLE_AUDIT_PROVIDER) -> dict[str, dict[str, int]]:
    summary: dict[str, dict[str, int]] = defaultdict(lambda: {"total": 0, "success": 0, "failure": 0})
    for event in (event if isinstance(event, AuditEvent) else AuditEvent.from_mapping(event) for event in events):
        if event.provider != provider:
            continue
        day = event.timestamp.date().isoformat()
        bucket = summary[day]
        bucket["total"] += 1
        if event.success:
            bucket["success"] += 1
        else:
            bucket["failure"] += 1
    return dict(sorted(summary.items()))


def format_audit_summary(summary: AuditSummary) -> dict[str, Any]:
    return {
        "provider": summary.provider,
        "provider_api_host": GOOGLE_AUDIT_API_HOST,
        "total_events": summary.total_events,
        "success_count": summary.success_count,
        "failure_count": summary.failure_count,
        "event_counts": summary.event_counts,
        "unique_subjects": summary.unique_subjects,
        "unique_emails": summary.unique_emails,
        "top_clients": summary.top_clients,
        "top_errors": summary.top_errors,
        "first_event_at": summary.first_event_at.isoformat() if summary.first_event_at else None,
        "last_event_at": summary.last_event_at.isoformat() if summary.last_event_at else None,
    }
