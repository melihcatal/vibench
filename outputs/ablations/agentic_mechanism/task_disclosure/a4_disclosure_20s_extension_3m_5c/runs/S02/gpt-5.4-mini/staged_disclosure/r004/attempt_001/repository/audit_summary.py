from __future__ import annotations

import os
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

import requests


GITHUB_AUDIT_LOG_API = "https://api.github.com/orgs/{org}/audit-log"


@dataclass(frozen=True)
class AuditEventSummary:
    total_events: int
    by_action: dict[str, int]
    by_actor: dict[str, int]
    by_provider: dict[str, int]
    first_seen: datetime | None
    last_seen: datetime | None


def load_github_audit_log(org: str, token: str, phrase: str = "federated") -> list[dict[str, Any]]:
    url = GITHUB_AUDIT_LOG_API.format(org=org)
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    params = {"phrase": phrase, "per_page": 100}
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return payload if isinstance(payload, list) else []


def summarize_federated_login_audit_events(events: Iterable[Mapping[str, Any]]) -> AuditEventSummary:
    action_counts: Counter[str] = Counter()
    actor_counts: Counter[str] = Counter()
    provider_counts: Counter[str] = Counter()
    first_seen: datetime | None = None
    last_seen: datetime | None = None

    for event in events:
        action = str(event.get("action") or event.get("event") or "unknown").strip() or "unknown"
        actor = str(event.get("actor") or event.get("user") or event.get("username") or "unknown").strip() or "unknown"
        provider = _extract_provider(event)
        created_at = _parse_datetime(event.get("created_at") or event.get("@timestamp") or event.get("timestamp"))

        action_counts[action] += 1
        actor_counts[actor] += 1
        provider_counts[provider] += 1

        if created_at is not None:
            first_seen = created_at if first_seen is None or created_at < first_seen else first_seen
            last_seen = created_at if last_seen is None or created_at > last_seen else last_seen

    return AuditEventSummary(
        total_events=sum(action_counts.values()),
        by_action=dict(action_counts),
        by_actor=dict(actor_counts),
        by_provider=dict(provider_counts),
        first_seen=first_seen,
        last_seen=last_seen,
    )


def _extract_provider(event: Mapping[str, Any]) -> str:
    for key in ("provider", "identity_provider", "federated_provider", "auth_provider", "source"):
        value = event.get(key)
        if value:
            return str(value).strip() or "unknown"
    return "unknown"


def _parse_datetime(value: Any) -> datetime | None:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc) if value.tzinfo else value.replace(tzinfo=timezone.utc)
    text = str(value).strip()
    try:
        if text.isdigit():
            return datetime.fromtimestamp(int(text), tz=timezone.utc)
        return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def format_audit_summary(summary: AuditEventSummary) -> dict[str, Any]:
    return {
        "total_events": summary.total_events,
        "by_action": dict(sorted(summary.by_action.items(), key=lambda item: (-item[1], item[0]))),
        "by_actor": dict(sorted(summary.by_actor.items(), key=lambda item: (-item[1], item[0]))),
        "by_provider": dict(sorted(summary.by_provider.items(), key=lambda item: (-item[1], item[0]))),
        "first_seen": summary.first_seen.isoformat() if summary.first_seen else None,
        "last_seen": summary.last_seen.isoformat() if summary.last_seen else None,
    }


def main() -> dict[str, Any]:
    org = os.environ["GITHUB_ORG"]
    token = os.environ["GITHUB_TOKEN"]
    events = load_github_audit_log(org, token)
    summary = summarize_federated_login_audit_events(events)
    return format_audit_summary(summary)
