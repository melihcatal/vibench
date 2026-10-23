from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import os
from typing import Any, Dict, Iterable, List, Mapping, Optional

import requests


AUTH0_API_BASE = "https://{tenant}.auth0.com/api/v2"


def _clean_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return str(value).strip() or None


def _to_datetime(value: Any) -> Optional[datetime]:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    text = str(value).strip()
    try:
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        parsed = datetime.fromisoformat(text)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    user_id: Optional[str] = None
    connection: Optional[str] = None
    client_id: Optional[str] = None
    ip: Optional[str] = None
    timestamp: Optional[datetime] = None
    success: Optional[bool] = None
    raw: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AuditEvent":
        return cls(
            event_type=_clean_str(data.get("type") or data.get("event_type") or data.get("event")) or "unknown",
            user_id=_clean_str(data.get("user_id") or data.get("user")),
            connection=_clean_str(data.get("connection") or data.get("connection_name") or data.get("provider")),
            client_id=_clean_str(data.get("client_id") or data.get("audience")),
            ip=_clean_str(data.get("ip") or data.get("ip_address") or data.get("origin_ip")),
            timestamp=_to_datetime(data.get("timestamp") or data.get("date") or data.get("created_at")),
            success=_parse_success(data),
            raw=dict(data),
        )


@dataclass(frozen=True)
class AuditSummary:
    total_events: int
    event_types: Dict[str, int]
    successes: int
    failures: int
    unique_users: int
    top_connections: List[Dict[str, Any]]
    first_seen: Optional[datetime]
    last_seen: Optional[datetime]
    raw: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "total_events": self.total_events,
            "event_types": self.event_types,
            "successes": self.successes,
            "failures": self.failures,
            "unique_users": self.unique_users,
            "top_connections": self.top_connections,
            "first_seen": self.first_seen.isoformat() if self.first_seen else None,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "raw": self.raw,
        }


def _parse_success(data: Mapping[str, Any]) -> Optional[bool]:
    for key in ("success", "succeeded", "result", "status"):
        value = data.get(key)
        if isinstance(value, bool):
            return value
        text = _clean_str(value)
        if text is None:
            continue
        lowered = text.lower()
        if lowered in {"success", "succeeded", "ok", "passed", "true", "1"}:
            return True
        if lowered in {"failure", "failed", "error", "false", "0"}:
            return False
    return None


def _load_events(payload: Any) -> List[AuditEvent]:
    if isinstance(payload, str):
        payload = json.loads(payload)
    if isinstance(payload, Mapping):
        items = payload.get("events") or payload.get("logs") or payload.get("items") or []
    else:
        items = payload
    return [AuditEvent.from_mapping(item) for item in items if isinstance(item, Mapping)]


def summarize_audit_events(events: Iterable[AuditEvent]) -> AuditSummary:
    total = 0
    event_types: Counter[str] = Counter()
    connections: Counter[str] = Counter()
    successes = 0
    failures = 0
    users = set()
    timestamps: List[datetime] = []
    raw_counts: Dict[str, int] = defaultdict(int)
    for event in events:
        total += 1
        event_types[event.event_type] += 1
        raw_counts[event.event_type] += 1
        if event.connection:
            connections[event.connection] += 1
        if event.user_id:
            users.add(event.user_id)
        if event.success is True:
            successes += 1
        elif event.success is False:
            failures += 1
        if event.timestamp:
            timestamps.append(event.timestamp)
    top_connections = [{"connection": name, "count": count} for name, count in connections.most_common(5)]
    return AuditSummary(
        total_events=total,
        event_types=dict(event_types),
        successes=successes,
        failures=failures,
        unique_users=len(users),
        top_connections=top_connections,
        first_seen=min(timestamps) if timestamps else None,
        last_seen=max(timestamps) if timestamps else None,
        raw={"event_type_counts": dict(raw_counts)},
    )


def fetch_auth0_audit_events(tenant: str, token: str, per_page: int = 50) -> List[AuditEvent]:
    base = AUTH0_API_BASE.format(tenant=tenant.strip())
    url = f"{base}/logs"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = requests.get(url, headers=headers, params={"per_page": per_page}, timeout=30)
    response.raise_for_status()
    return _load_events(response.json())


def build_auth0_summary_from_env() -> AuditSummary:
    tenant = os.environ["AUTH0_TENANT"]
    token = os.environ["AUTH0_MGMT_API_TOKEN"]
    events = fetch_auth0_audit_events(tenant=tenant, token=token)
    return summarize_audit_events(events)
