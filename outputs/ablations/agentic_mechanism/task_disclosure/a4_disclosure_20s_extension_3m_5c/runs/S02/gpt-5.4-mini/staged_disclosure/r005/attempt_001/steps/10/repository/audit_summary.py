from __future__ import annotations

import json
import os
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping, Sequence

import requests


GOOGLE_ADMIN_AUDIT_URL = "https://admin.googleapis.com/admin/reports/v1/activity/users/all/applications/login"


@dataclass(slots=True)
class AuditSummary:
    provider: str
    total_events: int
    successful_logins: int
    failed_logins: int
    unique_users: int
    top_failure_reasons: list[tuple[str, int]]
    events_by_day: dict[str, int]
    raw_events: list[dict[str, Any]]


def _env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or not str(value).strip():
        raise ValueError(f"Missing required environment variable: {name}")
    return str(value).strip()


def _parse_json_maybe(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return {}
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"value": text}
    return value


def _iter_google_login_events(payload: Mapping[str, Any]) -> Iterable[Mapping[str, Any]]:
    items = payload.get("items") or []
    for item in items:
        events = item.get("events") or []
        for event in events:
            yield event


def _extract_event_timestamp(event: Mapping[str, Any]) -> str | None:
    for key in ("id", "time", "timestamp", "date"):
        value = event.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, Mapping):
            for nested in ("time", "dateTime", "$t"):
                nested_value = value.get(nested)
                if isinstance(nested_value, str) and nested_value.strip():
                    return nested_value.strip()
    return None


def _extract_actor(event: Mapping[str, Any]) -> str | None:
    actor = event.get("actor") or event.get("user") or event.get("principal")
    if isinstance(actor, str) and actor.strip():
        return actor.strip()
    if isinstance(actor, Mapping):
        for key in ("email", "name", "id", "userKey"):
            value = actor.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    params = event.get("parameters") or []
    if isinstance(params, Sequence):
        for param in params:
            if not isinstance(param, Mapping):
                continue
            if str(param.get("name", "")).lower() in {"user", "email", "principal", "actor"}:
                value = param.get("value")
                if isinstance(value, str) and value.strip():
                    return value.strip()
    return None


def _extract_outcome(event: Mapping[str, Any]) -> str:
    for key in ("outcome", "status", "result", "event_name", "type"):
        value = event.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip().lower()
        if isinstance(value, Mapping):
            for nested in ("status", "value", "result"):
                nested_value = value.get(nested)
                if isinstance(nested_value, str) and nested_value.strip():
                    return nested_value.strip().lower()
    message = json.dumps(event, sort_keys=True).lower()
    if any(token in message for token in ("failure", "denied", "invalid", "error")):
        return "failure"
    return "success"


def _extract_failure_reason(event: Mapping[str, Any]) -> str | None:
    for key in ("reason", "error", "message", "description"):
        value = event.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, Mapping):
            for nested in ("message", "reason", "details"):
                nested_value = value.get(nested)
                if isinstance(nested_value, str) and nested_value.strip():
                    return nested_value.strip()
    return None


def summarize_federated_login_audits(events: Iterable[Mapping[str, Any]], provider: str = "google") -> AuditSummary:
    total_events = 0
    successful_logins = 0
    failed_logins = 0
    users = set()
    failure_reasons: Counter[str] = Counter()
    events_by_day: defaultdict[str, int] = defaultdict(int)
    raw_events: list[dict[str, Any]] = []

    for event in events:
        if not isinstance(event, Mapping):
            continue
        total_events += 1
        raw_events.append(dict(event))

        actor = _extract_actor(event)
        if actor:
            users.add(actor)

        timestamp = _extract_event_timestamp(event)
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                events_by_day[dt.date().isoformat()] += 1
            except ValueError:
                pass

        outcome = _extract_outcome(event)
        if outcome == "failure":
            failed_logins += 1
            reason = _extract_failure_reason(event)
            if reason:
                failure_reasons[reason] += 1
        else:
            successful_logins += 1

    return AuditSummary(
        provider=provider,
        total_events=total_events,
        successful_logins=successful_logins,
        failed_logins=failed_logins,
        unique_users=len(users),
        top_failure_reasons=failure_reasons.most_common(5),
        events_by_day=dict(sorted(events_by_day.items())),
        raw_events=raw_events,
    )


def fetch_google_audit_events() -> list[Mapping[str, Any]]:
    access_token = _env("GOOGLE_ACCESS_TOKEN")
    customer_id = _env("GOOGLE_CUSTOMER_ID", "my_customer")
    params = {
        "customerId": customer_id,
        "applicationName": "login",
        "maxResults": int(os.getenv("GOOGLE_AUDIT_MAX_RESULTS", "100")),
    }
    response = requests.get(
        GOOGLE_ADMIN_AUDIT_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return [event for event in _iter_google_login_events(payload)]


def build_audit_summary(payload: Mapping[str, Any] | str | None = None) -> AuditSummary:
    if payload is None:
        events = fetch_google_audit_events()
        return summarize_federated_login_audits(events, provider="google")
    data = _parse_json_maybe(payload)
    if isinstance(data, Mapping) and "items" in data:
        return summarize_federated_login_audits(_iter_google_login_events(data), provider="google")
    if isinstance(data, list):
        return summarize_federated_login_audits(data, provider="google")
    if isinstance(data, Mapping) and "events" in data:
        events = data.get("events") or []
        if isinstance(events, list):
            return summarize_federated_login_audits(events, provider="google")
    raise ValueError("Unsupported audit payload")


def summary_to_dict(summary: AuditSummary) -> dict[str, Any]:
    return {
        "provider": summary.provider,
        "total_events": summary.total_events,
        "successful_logins": summary.successful_logins,
        "failed_logins": summary.failed_logins,
        "unique_users": summary.unique_users,
        "top_failure_reasons": summary.top_failure_reasons,
        "events_by_day": summary.events_by_day,
    }


def main() -> None:
    summary = build_audit_summary()
    print(json.dumps(summary_to_dict(summary), sort_keys=True))


if __name__ == "__main__":
    main()
