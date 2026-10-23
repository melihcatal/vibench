import os
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional

import requests


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_MANAGEMENT_CLIENT_ID_ENV = "AUTH0_MANAGEMENT_CLIENT_ID"
AUTH0_MANAGEMENT_CLIENT_SECRET_ENV = "AUTH0_MANAGEMENT_CLIENT_SECRET"
AUTH0_MANAGEMENT_AUDIENCE_ENV = "AUTH0_MANAGEMENT_AUDIENCE"
AUTH0_LOGS_API_PATH = "/api/v2/logs"


@dataclass(frozen=True)
class AuditEventSummary:
    provider: str
    total_events: int
    event_counts: Dict[str, int]
    outcome_counts: Dict[str, int]
    user_counts: Dict[str, int]
    first_seen: Optional[str]
    last_seen: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "total_events": self.total_events,
            "event_counts": dict(self.event_counts),
            "outcome_counts": dict(self.outcome_counts),
            "user_counts": dict(self.user_counts),
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
        }


def _load_auth0_config(prefix: str = "AUTH0") -> Dict[str, Optional[str]]:
    return {
        "domain": os.getenv(f"{prefix}_DOMAIN"),
        "client_id": os.getenv(f"{prefix}_MANAGEMENT_CLIENT_ID"),
        "client_secret": os.getenv(f"{prefix}_MANAGEMENT_CLIENT_SECRET"),
        "audience": os.getenv(f"{prefix}_MANAGEMENT_AUDIENCE", f"https://{os.getenv(f'{prefix}_DOMAIN', '')}/api/v2/"),
    }


def _coerce_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _parse_timestamp(value: Any) -> Optional[datetime]:
    text = _coerce_text(value)
    if not text:
        return None
    normalized = text.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _format_timestamp(value: Optional[datetime]) -> Optional[str]:
    return value.isoformat().replace("+00:00", "Z") if value else None


def _extract_event_type(event: Mapping[str, Any]) -> str:
    return _coerce_text(event.get("type") or event.get("event_type") or event.get("eventType")) or "unknown"


def _extract_outcome(event: Mapping[str, Any]) -> str:
    error = _coerce_text(event.get("error") or event.get("description"))
    if error:
        return "failure"
    details = event.get("details")
    if isinstance(details, Mapping):
        if details.get("error") or details.get("error_description"):
            return "failure"
    return "success"


def _extract_user_id(event: Mapping[str, Any]) -> str:
    for key in ("user_id", "userId", "user", "sub", "username", "email"):
        value = _coerce_text(event.get(key))
        if value:
            return value
    return "unknown"


def summarize_audit_events(events: Iterable[Mapping[str, Any]]) -> AuditEventSummary:
    event_counts = Counter()
    outcome_counts = Counter()
    user_counts = Counter()
    timestamps: List[datetime] = []

    total = 0
    for event in events:
        total += 1
        event_counts[_extract_event_type(event)] += 1
        outcome_counts[_extract_outcome(event)] += 1
        user_counts[_extract_user_id(event)] += 1
        ts = _parse_timestamp(event.get("date") or event.get("timestamp") or event.get("created_at"))
        if ts:
            timestamps.append(ts)

    first_seen = _format_timestamp(min(timestamps)) if timestamps else None
    last_seen = _format_timestamp(max(timestamps)) if timestamps else None
    return AuditEventSummary(
        provider="Auth0",
        total_events=total,
        event_counts=dict(event_counts),
        outcome_counts=dict(outcome_counts),
        user_counts=dict(user_counts),
        first_seen=first_seen,
        last_seen=last_seen,
    )


def _get_auth0_management_token(config: Mapping[str, Optional[str]], timeout: float = 30.0) -> str:
    domain = config.get("domain") or ""
    client_id = config.get("client_id") or ""
    client_secret = config.get("client_secret") or ""
    audience = config.get("audience") or f"https://{domain}/api/v2/"
    if not domain or not client_id or not client_secret:
        raise ValueError("AUTH0_DOMAIN, AUTH0_MANAGEMENT_CLIENT_ID, and AUTH0_MANAGEMENT_CLIENT_SECRET are required")
    response = requests.post(
        f"https://{domain}/oauth/token",
        json={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "audience": audience,
        },
        headers={"content-type": "application/json"},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    token = _coerce_text(payload.get("access_token"))
    if not token:
        raise ValueError("Auth0 management token response missing access_token")
    return token


def fetch_auth0_audit_events(per_page: int = 100, page: int = 0, timeout: float = 30.0) -> List[Dict[str, Any]]:
    config = _load_auth0_config()
    domain = config.get("domain") or ""
    token = _get_auth0_management_token(config, timeout=timeout)
    response = requests.get(
        f"https://{domain}{AUTH0_LOGS_API_PATH}",
        params={"per_page": per_page, "page": page},
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    return list(data) if isinstance(data, list) else []


def summarize_auth0_audit_events(per_page: int = 100, page: int = 0, timeout: float = 30.0) -> Dict[str, Any]:
    events = fetch_auth0_audit_events(per_page=per_page, page=page, timeout=timeout)
    return summarize_audit_events(events).to_dict()
