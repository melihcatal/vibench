"""
audit_summary.py - Summarize federated-login audit events using Datadog Logs API
to query and aggregate Auth0 audit log events.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timedelta, timezone

import requests

from identity_client import AUTH0_DOMAIN
from identity_models import build_audit_record

logger = logging.getLogger(__name__)

DATADOG_API_KEY = os.getenv("DATADOG_API_KEY", "")
DATADOG_APP_KEY = os.getenv("DATADOG_APP_KEY", "")
DATADOG_SITE = os.getenv("DATADOG_SITE", "datadoghq.com")
DATADOG_BASE_URL = f"https://api.{DATADOG_SITE}"


def query_auth0_audit_events(
    from_ts: datetime,
    to_ts: datetime,
    event_type: str | None = None,
    api_key: str = DATADOG_API_KEY,
    app_key: str = DATADOG_APP_KEY,
) -> list[dict]:
    """
    Query Auth0 federated-login audit events from Datadog Logs API.
    Auth0 logs are streamed to Datadog via the Auth0-Datadog integration.
    """
    logs_search_url = f"{DATADOG_BASE_URL}/api/v2/logs/events/search"
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Content-Type": "application/json",
    }

    query = f"source:auth0 service:auth0-authentication @event_type:login"
    if event_type:
        query += f" @event_type:{event_type}"

    payload = {
        "filter": {
            "query": query,
            "from": from_ts.isoformat(),
            "to": to_ts.isoformat(),
        },
        "sort": "-timestamp",
        "page": {"limit": 100},
    }

    response = requests.post(logs_search_url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("data", [])


def build_audit_summary(
    events: list[dict],
    window_hours: int = 24,
) -> dict:
    """
    Build a summary of federated-login audit events collected from Datadog.
    """
    total = len(events)
    successes = 0
    failures = 0
    connections: dict[str, int] = {}
    providers: dict[str, int] = {}
    unique_users: set[str] = set()

    for event in events:
        attributes = event.get("attributes", {})
        tags = attributes.get("tags", [])
        event_type = attributes.get("event_type", "unknown")
        connection = attributes.get("details", {}).get("connection", "unknown")
        provider = attributes.get("provider", "auth0")
        user_id = attributes.get("user_id", attributes.get("user_name", ""))

        if event_type in ("success", "succeeded", "login"):
            successes += 1
        else:
            failures += 1

        connections[connection] = connections.get(connection, 0) + 1
        providers[provider] = providers.get(provider, 0) + 1
        if user_id:
            unique_users.add(user_id)

    return {
        "window_hours": window_hours,
        "total_events": total,
        "successes": successes,
        "failures": failures,
        "success_rate": round(successes / total, 4) if total else 0,
        "connections_breakdown": connections,
        "providers_breakdown": providers,
        "unique_users": len(unique_users),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def generate_audit_report(
    hours: int = 24,
    api_key: str = DATADOG_API_KEY,
    app_key: str = DATADOG_APP_KEY,
) -> dict:
    """Generate a full audit summary report from Datadog for Auth0 events."""
    to_ts = datetime.now(timezone.utc)
    from_ts = to_ts - timedelta(hours=hours)

    events = query_auth0_audit_events(from_ts, to_ts, api_key=api_key, app_key=app_key)
    summary = build_audit_summary(events, window_hours=hours)
    summary["source"] = "datadog"
    summary["auth0_domain"] = AUTH0_DOMAIN
    return summary


if __name__ == "__main__":
    report = generate_audit_report(hours=1)
    print(json.dumps(report, indent=2, default=str))
