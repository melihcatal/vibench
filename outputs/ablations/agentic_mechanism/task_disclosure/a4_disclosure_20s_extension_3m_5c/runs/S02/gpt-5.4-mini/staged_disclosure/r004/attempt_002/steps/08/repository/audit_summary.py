from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping, Optional

try:
    from identity_models import FederatedLoginResponse
except Exception:
    FederatedLoginResponse = None  # type: ignore[assignment]

import requests


IDENTITY_PROVIDER = "auth0"
AUTH0_AUDIT_LOGS_URL = "https://{tenant}.auth0.com/api/v2/logs"


@dataclass(frozen=True)
class AuditEvent:
    provider: str
    user_id: str
    event_type: str
    timestamp: datetime
    success: bool
    ip_address: Optional[str] = None
    description: Optional[str] = None
    raw: Mapping[str, Any] = None  # type: ignore[assignment]


def _parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc) if value.tzinfo else value.replace(tzinfo=timezone.utc)
    text = str(value).strip()
    parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    return parsed.astimezone(timezone.utc) if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _clean_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def fetch_auth0_audit_events(tenant: str, api_token: str, per_page: int = 100) -> list[Mapping[str, Any]]:
    url = AUTH0_AUDIT_LOGS_URL.format(tenant=tenant)
    headers = {"Authorization": f"Bearer {api_token}"}
    params = {"per_page": per_page, "sort": "date:-1"}
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return payload if isinstance(payload, list) else payload.get("logs", [])


def normalize_auth0_event(event: Mapping[str, Any]) -> AuditEvent:
    user_id = _clean_text(event.get("user_id") or event.get("userId") or event.get("user")) or "unknown"
    event_type = _clean_text(event.get("type") or event.get("event_type")) or "unknown"
    timestamp = _parse_datetime(event.get("date") or event.get("timestamp") or event.get("created_at") or datetime.now(timezone.utc))
    success = bool(event.get("success", event.get("is_success", True)))
    return AuditEvent(
        provider=IDENTITY_PROVIDER,
        user_id=user_id,
        event_type=event_type,
        timestamp=timestamp,
        success=success,
        ip_address=_clean_text(event.get("ip") or event.get("ip_address")),
        description=_clean_text(event.get("description") or event.get("details")),
        raw=dict(event),
    )


def summarize_audit_events(events: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    normalized = [normalize_auth0_event(event) for event in events]
    by_type = Counter(event.event_type for event in normalized)
    by_user = Counter(event.user_id for event in normalized)
    failed = sum(1 for event in normalized if not event.success)
    last_seen = max((event.timestamp for event in normalized), default=None)
    first_seen = min((event.timestamp for event in normalized), default=None)
    active_users = len(by_user)
    return {
        "provider": IDENTITY_PROVIDER,
        "total_events": len(normalized),
        "failed_events": failed,
        "active_users": active_users,
        "event_types": dict(by_type),
        "events_per_user": dict(by_user),
        "first_seen": first_seen.isoformat() if first_seen else None,
        "last_seen": last_seen.isoformat() if last_seen else None,
    }


def summarize_federated_login_audit(tenant: str, api_token: str) -> dict[str, Any]:
    events = fetch_auth0_audit_events(tenant, api_token)
    summary = summarize_audit_events(events)
    summary["provider"] = IDENTITY_PROVIDER
    if FederatedLoginResponse is not None:
        summary["integration"] = "identity_models.FederatedLoginResponse"
    return summary
