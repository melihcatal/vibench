import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional

import requests

AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_AUDIT_LOGS_PATH = "/api/v2/logs"
AUTH0_AUDIT_LOGS_PAGE_SIZE = 100


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def _parse_iso_datetime(value: Any) -> Optional[datetime]:
    text = _normalize_text(value)
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class AuditEvent:
    event_id: str = ""
    event_type: str = ""
    description: str = ""
    user_id: str = ""
    client_id: str = ""
    connection_id: str = ""
    ip: str = ""
    user_agent: str = ""
    timestamp: Optional[datetime] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_mapping(data: Mapping[str, Any]) -> "AuditEvent":
        return AuditEvent(
            event_id=_normalize_text(data.get("log_id") or data.get("id")),
            event_type=_normalize_text(data.get("type") or data.get("event_type")),
            description=_normalize_text(data.get("description") or data.get("details")),
            user_id=_normalize_text((data.get("user_id") or data.get("user") or {}).get("user_id") if isinstance(data.get("user"), Mapping) else data.get("user_id")),
            client_id=_normalize_text(data.get("client_id")),
            connection_id=_normalize_text(data.get("connection_id") or data.get("connection")),
            ip=_normalize_text(data.get("ip") or data.get("ip_address")),
            user_agent=_normalize_text(data.get("user_agent") or data.get("user_agent_details")),
            timestamp=_parse_iso_datetime(data.get("date") or data.get("timestamp") or data.get("created_at")),
            raw=dict(data),
        )


@dataclass(frozen=True)
class AuditSummary:
    total_events: int
    event_types: Dict[str, int]
    users: Dict[str, int]
    clients: Dict[str, int]
    connections: Dict[str, int]
    first_seen: Optional[str]
    last_seen: Optional[str]
    error_events: int
    raw_events: List[Dict[str, Any]]


class Auth0AuditClient:
    def __init__(self, domain: Optional[str] = None, token: Optional[str] = None, session: Optional[requests.Session] = None):
        self.domain = domain or __import__("os").getenv(AUTH0_DOMAIN_ENV, "")
        self.token = token or __import__("os").getenv("AUTH0_MGMT_API_TOKEN", "")
        self.session = session or requests.Session()
        if not self.domain:
            raise ValueError("AUTH0_DOMAIN is required")
        if not self.token:
            raise ValueError("AUTH0_MGMT_API_TOKEN is required")

    @property
    def base_url(self) -> str:
        return f"https://{self.domain.rstrip('/')}"

    @property
    def logs_url(self) -> str:
        return f"{self.base_url}{AUTH0_AUDIT_LOGS_PATH}"

    def list_events(self, take: int = AUTH0_AUDIT_LOGS_PAGE_SIZE) -> List[Dict[str, Any]]:
        response = self.session.get(
            self.logs_url,
            headers={"Authorization": f"Bearer {self.token}", "Accept": "application/json"},
            params={"take": take},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        if isinstance(payload, list):
            return payload
        if isinstance(payload, Mapping) and isinstance(payload.get("logs"), list):
            return payload["logs"]
        return []


def summarize_audit_events(events: Iterable[Mapping[str, Any]]) -> AuditSummary:
    parsed_events = [AuditEvent.from_mapping(event) for event in events]
    event_types = Counter()
    users = Counter()
    clients = Counter()
    connections = Counter()
    error_events = 0
    timestamps: List[datetime] = []

    for event in parsed_events:
        if event.event_type:
            event_types[event.event_type] += 1
        if event.user_id:
            users[event.user_id] += 1
        if event.client_id:
            clients[event.client_id] += 1
        if event.connection_id:
            connections[event.connection_id] += 1
        if event.timestamp:
            timestamps.append(event.timestamp)
        if event.event_type.startswith("f") or "error" in event.event_type.lower() or "failure" in event.event_type.lower():
            error_events += 1

    first_seen = min(timestamps).isoformat() if timestamps else None
    last_seen = max(timestamps).isoformat() if timestamps else None
    return AuditSummary(
        total_events=len(parsed_events),
        event_types=dict(event_types),
        users=dict(users),
        clients=dict(clients),
        connections=dict(connections),
        first_seen=first_seen,
        last_seen=last_seen,
        error_events=error_events,
        raw_events=[event.raw for event in parsed_events],
    )


def fetch_and_summarize_audit_events(domain: Optional[str] = None, token: Optional[str] = None, take: int = AUTH0_AUDIT_LOGS_PAGE_SIZE) -> AuditSummary:
    client = Auth0AuditClient(domain=domain, token=token)
    return summarize_audit_events(client.list_events(take=take))


def summarize_audit_events_as_json(events: Iterable[Mapping[str, Any]]) -> str:
    summary = summarize_audit_events(events)
    return json.dumps(
        {
            "total_events": summary.total_events,
            "event_types": summary.event_types,
            "users": summary.users,
            "clients": summary.clients,
            "connections": summary.connections,
            "first_seen": summary.first_seen,
            "last_seen": summary.last_seen,
            "error_events": summary.error_events,
        },
        sort_keys=True,
    )
