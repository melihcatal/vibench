"""
Summarize federated-login audit events using Datadog Logs API.

Provider: Datadog Log Management API (https://docs.datadoghq.com/api/latest/logs/)
"""

import os
import time
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from datadog_api_client import Configuration
from datadog_api_client.v1.api.logs_api import LogsApi
from datadog_api_client.v1.model.logs_list_request import LogsListRequest
from datadog_api_client.v1.model.logs_list_request_time import LogsListRequestTime
from datadog_api_client.v1.model.logs_query_filter import LogsQueryFilter


DATADOG_API_KEY = os.getenv("DATADOG_API_KEY", "")
DATADOG_APP_KEY = os.getenv("DATADOG_APP_KEY", "")
DATADOG_SITE = os.getenv("DATADOG_SITE", "datadoghq.com")

# Datadog log index for federated login events
LOGIN_LOG_INDEX = os.getenv("DATADOG_LOGIN_LOG_INDEX", "federated-login")
LOGIN_LOG_SOURCE = os.getenv("DATADOG_LOGIN_LOG_SOURCE", "oauth-service")


class DatadogAuditError(Exception):
    """Raised when Datadog API call fails."""
    pass


def init_datadog_config() -> Configuration:
    """Initialize Datadog API client configuration."""
    config = Configuration()
    config.api_key["apiKeyAuth"] = DATADOG_API_KEY
    config.api_key["appKeyAuth"] = DATADOG_APP_KEY
    config.server_variables = {"site": DATADOG_SITE}
    return config


def build_login_query(
    provider: Optional[str] = None,
    session_id: Optional[str] = None,
    user_email: Optional[str] = None,
    time_from: Optional[int] = None,
    time_to: Optional[int] = None,
) -> str:
    """
    Build Datadog log query for federated login events.

    Uses Datadog log search syntax with source, service, and attribute filters.
    """
    filters = [
        f"source:{LOGIN_LOG_SOURCE}",
    ]

    if provider:
        filters.append(f"@provider:{provider}")
    if session_id:
        filters.append(f"@session_id:{session_id}")
    if user_email:
        filters.append(f"@user.email:{user_email}")

    return " ".join(filters)


def query_login_events(
    time_window_hours: int = 24,
    provider: Optional[str] = None,
    limit: int = 1000,
) -> List[Dict]:
    """
    Query Datadog for federated login audit events.

    Uses Datadog Logs API /api/v1/logs-archives/search endpoint.
    """
    try:
        config = init_datadog_config()
        with LogsApi(config) as api:
            time_from = int((datetime.utcnow() - timedelta(hours=time_window_hours)).timestamp())
            time_to = int(datetime.utcnow().timestamp())

            query = build_login_query(provider=provider)

            body = LogsListRequest(
                filter=LogsListRequestTime(
                    _from=time_from,
                    to=time_to,
                    query=query,
                ),
                sort="timestamp",
                limit=limit,
            )

            response = api.list_logs(body=body)
            events = []

            for log in response.logs:
                events.append({
                    "timestamp": log.attributes.get("timestamp"),
                    "message": log.attributes.get("message"),
                    "status": log.attributes.get("status"),
                    "provider": log.attributes.get("provider"),
                    "session_id": log.attributes.get("session_id"),
                    "user_email": log.attributes.get("user", {}).get("email"),
                    "action": log.attributes.get("action"),
                    "ip_address": log.attributes.get("network", {}).get("client", {}).get("ip"),
                })

            return events

    except Exception as e:
        raise DatadogAuditError(f"Datadog query failed: {str(e)}")


def summarize_login_events(
    events: List[Dict],
) -> Dict:
    """
    Summarize federated login audit events into aggregated statistics.

    Returns counts by provider, action, success/failure, and time distribution.
    """
    summary = {
        "total_events": len(events),
        "by_provider": {},
        "by_action": {},
        "success_count": 0,
        "failure_count": 0,
        "unique_sessions": set(),
        "unique_users": set(),
        "time_range": {
            "earliest": None,
            "latest": None,
        },
    }

    for event in events:
        # Provider breakdown
        provider = event.get("provider", "unknown")
        summary["by_provider"][provider] = summary["by_provider"].get(provider, 0) + 1

        # Action breakdown
        action = event.get("action", "unknown")
        summary["by_action"][action] = summary["by_action"].get(action, 0) + 1

        # Success/failure
        status = event.get("status", "")
        if status in ("error", "failure", "fail"):
            summary["failure_count"] += 1
        else:
            summary["success_count"] += 1

        # Unique tracking
        if event.get("session_id"):
            summary["unique_sessions"].add(event["session_id"])
        if event.get("user_email"):
            summary["unique_users"].add(event["user_email"])

        # Time range
        ts = event.get("timestamp")
        if ts:
            if summary["time_range"]["earliest"] is None or ts < summary["time_range"]["earliest"]:
                summary["time_range"]["earliest"] = ts
            if summary["time_range"]["latest"] is None or ts > summary["time_range"]["latest"]:
                summary["time_range"]["latest"] = ts

    # Convert sets to counts for serialization
    summary["unique_session_count"] = len(summary["unique_sessions"])
    summary["unique_user_count"] = len(summary["unique_users"])
    del summary["unique_sessions"]
    del summary["unique_users"]

    return summary


def get_audit_summary(
    time_window_hours: int = 24,
    provider: Optional[str] = None,
) -> Dict:
    """
    Get federated login audit summary from Datadog.

    Queries Datadog Logs API and returns aggregated statistics.
    """
    events = query_login_events(
        time_window_hours=time_window_hours,
        provider=provider,
    )
    return summarize_login_events(events)


if __name__ == "__main__":
    import json
    summary = get_audit_summary(time_window_hours=24)
    print(json.dumps(summary, indent=2))
