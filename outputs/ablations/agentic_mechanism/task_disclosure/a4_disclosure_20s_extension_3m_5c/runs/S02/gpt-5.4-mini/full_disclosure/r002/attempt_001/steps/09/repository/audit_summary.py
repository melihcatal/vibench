import json
import os
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional

import requests


OKTA_AUDIT_LOGS_ENDPOINT = "https://{org}/api/v1/logs"


@dataclass(frozen=True)
class AuditEventSummary:
    provider: str
    total_events: int
    event_types: Dict[str, int]
    outcomes: Dict[str, int]
    actors: Dict[str, int]
    first_seen: Optional[str]
    last_seen: Optional[str]
    raw: Dict[str, Any]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _string_or_none(value: Any) -> Optional[str]:
    if isinstance(value, str):
        value = value.strip()
        return value or None
    if value is None:
        return None
    return str(value)


def _event_timestamp(event: Mapping[str, Any]) -> Optional[datetime]:
    for key in ("published", "timestamp", "eventTime", "occurred_at", "createdAt"):
        raw = event.get(key)
        if not raw:
            continue
        if isinstance(raw, datetime):
            return raw.astimezone(timezone.utc)
        if isinstance(raw, str):
            candidate = raw.replace("Z", "+00:00")
            try:
                dt = datetime.fromisoformat(candidate)
            except ValueError:
                continue
            return dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    return None


def _actor_key(event: Mapping[str, Any]) -> str:
    actor = event.get("actor") or {}
    if isinstance(actor, Mapping):
        for key in ("displayName", "alternateId", "id", "email", "login"):
            value = _string_or_none(actor.get(key))
            if value:
                return value
    return "unknown"


def _event_type(event: Mapping[str, Any]) -> str:
    for key in ("eventType", "type", "action", "event_type"):
        value = _string_or_none(event.get(key))
        if value:
            return value
    return "unknown"


def _outcome(event: Mapping[str, Any]) -> str:
    outcome = event.get("outcome")
    if isinstance(outcome, Mapping):
        for key in ("result", "status"):
            value = _string_or_none(outcome.get(key))
            if value:
                return value
    for key in ("result", "status", "outcome"):
        value = _string_or_none(event.get(key))
        if value:
            return value
    return "unknown"


def fetch_okta_audit_events(org_domain: str, api_token: str, limit: int = 200) -> List[Dict[str, Any]]:
    url = OKTA_AUDIT_LOGS_ENDPOINT.format(org=org_domain.strip())
    response = requests.get(
        url,
        headers={"Authorization": f"SSWS {api_token}", "Accept": "application/json"},
        params={"limit": str(limit)},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, list):
        return [event for event in payload if isinstance(event, dict)]
    if isinstance(payload, dict):
        embedded = payload.get("events") or payload.get("items") or payload.get("data")
        if isinstance(embedded, list):
            return [event for event in embedded if isinstance(event, dict)]
    raise ValueError("unexpected_okta_audit_payload")


def summarize_federated_login_audit_events(events: Iterable[Mapping[str, Any]]) -> AuditEventSummary:
    event_list = [event for event in events if isinstance(event, Mapping)]
    event_types = Counter()
    outcomes = Counter()
    actors = Counter()
    timestamps: List[datetime] = []

    for event in event_list:
        event_types[_event_type(event)] += 1
        outcomes[_outcome(event)] += 1
        actors[_actor_key(event)] += 1
        ts = _event_timestamp(event)
        if ts is not None:
            timestamps.append(ts)

    first_seen = min(timestamps).isoformat() if timestamps else None
    last_seen = max(timestamps).isoformat() if timestamps else None
    return AuditEventSummary(
        provider="okta",
        total_events=len(event_list),
        event_types=dict(event_types),
        outcomes=dict(outcomes),
        actors=dict(actors),
        first_seen=first_seen,
        last_seen=last_seen,
        raw={"generated_at": _utc_now_iso()},
    )


def summarize_okta_audit_events(org_domain: str, api_token: str, limit: int = 200) -> AuditEventSummary:
    return summarize_federated_login_audit_events(fetch_okta_audit_events(org_domain, api_token, limit=limit))


def summary_to_dict(summary: AuditEventSummary) -> Dict[str, Any]:
    return {
        "provider": summary.provider,
        "total_events": summary.total_events,
        "event_types": summary.event_types,
        "outcomes": summary.outcomes,
        "actors": summary.actors,
        "first_seen": summary.first_seen,
        "last_seen": summary.last_seen,
        "raw": summary.raw,
    }


def main() -> None:
    org_domain = os.environ.get("OKTA_ORG_DOMAIN") or os.environ.get("OKTA_DOMAIN")
    api_token = os.environ.get("OKTA_API_TOKEN")
    if not org_domain or not api_token:
        raise ValueError("missing_okta_configuration")
    summary = summarize_okta_audit_events(org_domain, api_token)
    print(json.dumps(summary_to_dict(summary), sort_keys=True))


if __name__ == "__main__":
    main()
