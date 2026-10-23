from __future__ import annotations

import json
import os
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional

import requests


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_GRAFANA_WORKSPACE_ID = os.getenv("AWS_GRAFANA_WORKSPACE_ID", "")
AWS_GRAFANA_API_BASE = f"https://grafana-workspace.{AWS_REGION}.amazonaws.com"


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    provider: str
    subject: str
    outcome: str
    timestamp: datetime
    raw: Mapping[str, Any]


def _parse_timestamp(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc)
    if isinstance(value, str):
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        return datetime.fromisoformat(text).astimezone(timezone.utc)
    return datetime.now(timezone.utc)


def normalize_event(record: Mapping[str, Any]) -> AuditEvent:
    provider = str(record.get("provider") or record.get("idp") or "aws-grafana")
    event_type = str(record.get("event_type") or record.get("type") or "unknown")
    subject = str(record.get("subject") or record.get("user") or record.get("user_id") or "unknown")
    outcome = str(record.get("outcome") or record.get("status") or "unknown")
    timestamp = _parse_timestamp(record.get("timestamp") or record.get("time") or record.get("created_at"))
    return AuditEvent(
        event_type=event_type,
        provider=provider,
        subject=subject,
        outcome=outcome,
        timestamp=timestamp,
        raw=record,
    )


def summarize_audit_events(records: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    events = [normalize_event(r) for r in records]
    total = len(events)
    by_type = Counter(event.event_type for event in events)
    by_outcome = Counter(event.outcome for event in events)
    by_provider = Counter(event.provider for event in events)
    subjects = Counter(event.subject for event in events)
    first_seen = min((event.timestamp for event in events), default=None)
    last_seen = max((event.timestamp for event in events), default=None)

    failures_by_type = defaultdict(int)
    for event in events:
        if event.outcome.lower() not in {"success", "ok", "passed", "allow"}:
            failures_by_type[event.event_type] += 1

    return {
        "total_events": total,
        "providers": dict(by_provider),
        "event_types": dict(by_type),
        "outcomes": dict(by_outcome),
        "top_subjects": subjects.most_common(10),
        "failures_by_type": dict(failures_by_type),
        "first_seen": first_seen.isoformat() if first_seen else None,
        "last_seen": last_seen.isoformat() if last_seen else None,
    }


def fetch_audit_events(limit: int = 100) -> List[Mapping[str, Any]]:
    if not AWS_GRAFANA_WORKSPACE_ID:
        return []
    url = f"{AWS_GRAFANA_API_BASE}/workspaces/{AWS_GRAFANA_WORKSPACE_ID}/audit-events"
    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        params={"limit": limit},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("items", "events", "records", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def summarize_federated_login_audit(limit: int = 100) -> Dict[str, Any]:
    return summarize_audit_events(fetch_audit_events(limit=limit))


def main() -> None:
    summary = summarize_federated_login_audit()
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
