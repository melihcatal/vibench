import os
import time
import requests
from typing import Optional, Dict, Any, List
from identity_models import (
    AuditSummary,
    AuditEvent,
    AuditEventType,
)


DATADOG_API_URL = "https://api.datadoghq.com"
DATADOG_LOGS_API_URL = "https://http-intake.logs.datadoghq.com"


def query_datadog_audit_events(
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
    query: str = "service:federated-login",
    time_from: Optional[int] = None,
    time_to: Optional[int] = None,
    limit: int = 1000,
) -> List[Dict[str, Any]]:
    if api_key is None:
        api_key = os.environ.get("DATADOG_API_KEY", "")
    if app_key is None:
        app_key = os.environ.get("DATADOG_APP_KEY", "")

    if not api_key:
        raise ValueError("DATADOG_API_KEY environment variable is required")

    if time_from is None:
        time_from = int(time.time()) - 86400
    if time_to is None:
        time_to = int(time.time())

    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Content-Type": "application/json",
    }

    body = {
        "filter": {
            "query": query,
            "from": time_from,
            "to": time_to,
        },
        "sort": "timestamp",
        "page": {
            "limit": limit,
        },
    }

    response = requests.post(
        f"{DATADOG_API_URL}/api/v2/logs/events/search",
        headers=headers,
        json=body,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    events = []
    for log_entry in data.get("data", []):
        attributes = log_entry.get("attributes", {})
        events.append(
            {
                "timestamp": attributes.get("timestamp"),
                "message": attributes.get("message", ""),
                "status": attributes.get("status", "info"),
                "service": attributes.get("service", ""),
                "tags": attributes.get("tags", []),
                "attributes": attributes.get("attributes", {}),
            }
        )

    return events


def summarize_federated_login_audit(
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
    time_window_seconds: int = 86400,
    query_filter: str = "service:federated-login",
) -> AuditSummary:
    time_to = int(time.time())
    time_from = time_to - time_window_seconds

    events = query_datadog_audit_events(
        api_key=api_key,
        app_key=app_key,
        query=query_filter,
        time_from=time_from,
        time_to=time_to,
    )

    summary = AuditSummary(
        total_events=len(events),
        time_range={"from": time_from, "to": time_to},
        raw_events=events,
    )

    events_by_type: Dict[str, int] = {}
    events_by_status: Dict[str, int] = {}
    events_by_provider: Dict[str, int] = {}
    unique_users = set()

    for event in events:
        status = event.get("status", "unknown")
        events_by_status[status] = events_by_status.get(status, 0) + 1

        attributes = event.get("attributes", {})
        event_type = attributes.get("event_type", "unknown")
        events_by_type[event_type] = events_by_type.get(event_type, 0) + 1

        provider = attributes.get("provider", "unknown")
        events_by_provider[provider] = events_by_provider.get(provider, 0) + 1

        user_sub = attributes.get("user_sub")
        if user_sub:
            unique_users.add(user_sub)

    summary.events_by_type = events_by_type
    summary.events_by_status = events_by_status
    summary.events_by_provider = events_by_provider
    summary.unique_users = len(unique_users)

    return summary


def get_datadog_login_metrics(
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
    metric_name: str = "federated.login.count",
    time_window_seconds: int = 3600,
) -> Dict[str, Any]:
    if api_key is None:
        api_key = os.environ.get("DATADOG_API_KEY", "")
    if app_key is None:
        app_key = os.environ.get("DATADOG_APP_KEY", "")

    if not api_key:
        raise ValueError("DATADOG_API_KEY environment variable is required")

    time_to = int(time.time())
    time_from = time_to - time_window_seconds

    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Content-Type": "application/json",
    }

    response = requests.get(
        f"{DATADOG_API_URL}/api/v1/query",
        headers=headers,
        params={
            "from": time_from,
            "to": time_to,
            "query": f"avg:{metric_name}{{*}}",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def send_audit_event_to_datadog(
    event: AuditEvent,
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
) -> Dict[str, Any]:
    if api_key is None:
        api_key = os.environ.get("DATADOG_API_KEY", "")

    if not api_key:
        raise ValueError("DATADOG_API_KEY environment variable is required")

    headers = {
        "DD-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    log_payload = {
        "ddsource": "federated-login",
        "service": "federated-login",
        "hostname": os.environ.get("HOSTNAME", "unknown"),
        "message": f"Federated login event: {event.event_type}",
        "status": "info" if event.status == "success" else "error",
        "ddtags": f"event_type:{event.event_type},provider:{event.provider},status:{event.status}",
        "event_type": event.event_type,
        "user_sub": event.user_sub,
        "session_id": event.session_id,
        "provider": event.provider,
        "ip_address": event.ip_address,
        "details": event.details,
    }

    response = requests.post(
        DATADOG_LOGS_API_URL,
        headers=headers,
        json=log_payload,
        timeout=30,
    )
    response.raise_for_status()

    return {
        "success": True,
        "event_id": event.event_id,
        "status_code": response.status_code,
    }
