import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from datadog import initialize, statsd
from identity_models import AuditEvent


def initialize_datadog():
    """Initialize Datadog metrics client."""
    options = {
        "statsd_host": os.getenv("DATADOG_AGENT_HOST", "localhost"),
        "statsd_port": int(os.getenv("DATADOG_AGENT_PORT", 8125)),
        "api_key": os.getenv("DATADOG_API_KEY", ""),
        "app_key": os.getenv("DATADOG_APP_KEY", ""),
    }
    initialize(**options)


def summarize_login_audit_events(events: List[AuditEvent], time_window_hours: int = 24):
    """Summarize federated login audit events using Datadog metrics."""
    initialize_datadog()

    now = datetime.now()
    window_start = now - timedelta(hours=time_window_hours)

    recent_events = [e for e in events if e.timestamp >= window_start]

    summary = {
        "total_events": len(recent_events),
        "successful_logins": sum(
            1 for e in recent_events if e.success and e.event_type == "login"
        ),
        "failed_logins": sum(
            1 for e in recent_events if not e.success and e.event_type == "login"
        ),
        "unique_users": len(set(e.user_id for e in recent_events if e.user_id)),
        "providers": {},
        "hourly_breakdown": {},
    }

    for event in recent_events:
        provider = event.provider or "unknown"
        summary["providers"][provider] = summary["providers"].get(provider, 0) + 1

        hour_key = event.timestamp.strftime("%Y-%m-%d %H:00")
        summary["hourly_breakdown"][hour_key] = (
            summary["hourly_breakdown"].get(hour_key, 0) + 1
        )

    send_datadog_metrics(summary, time_window_hours)

    return summary


def send_datadog_metrics(summary: Dict[str, Any], time_window_hours: int):
    """Send audit summary metrics to Datadog."""
    tags = [
        f"time_window:{time_window_hours}h",
        "service:federated_login",
        "env:" + os.getenv("ENVIRONMENT", "development"),
    ]

    statsd.gauge(
        "federated_login.audit.total_events", summary["total_events"], tags=tags
    )
    statsd.gauge(
        "federated_login.audit.successful_logins",
        summary["successful_logins"],
        tags=tags,
    )
    statsd.gauge(
        "federated_login.audit.failed_logins", summary["failed_logins"], tags=tags
    )
    statsd.gauge(
        "federated_login.audit.unique_users", summary["unique_users"], tags=tags
    )

    for provider, count in summary["providers"].items():
        provider_tags = tags + [f"provider:{provider}"]
        statsd.gauge("federated_login.audit.by_provider", count, tags=provider_tags)

    error_rate = 0
    if summary["total_events"] > 0:
        error_rate = summary["failed_logins"] / summary["total_events"] * 100

    statsd.gauge("federated_login.audit.error_rate_percent", error_rate, tags=tags)


def generate_audit_report(events: List[AuditEvent], report_type: str = "daily"):
    """Generate detailed audit report."""
    if report_type == "daily":
        window = timedelta(days=1)
    elif report_type == "weekly":
        window = timedelta(days=7)
    elif report_type == "monthly":
        window = timedelta(days=30)
    else:
        window = timedelta(hours=24)

    now = datetime.now()
    window_start = now - window

    filtered_events = [e for e in events if e.timestamp >= window_start]

    report = {
        "report_type": report_type,
        "time_period": {"start": window_start.isoformat(), "end": now.isoformat()},
        "summary": summarize_login_audit_events(
            filtered_events, time_window_hours=window.total_seconds() // 3600
        ),
        "top_users": get_top_users(filtered_events, limit=10),
        "common_errors": get_common_errors(filtered_events, limit=5),
        "provider_breakdown": get_provider_breakdown(filtered_events),
    }

    send_datadog_custom_metrics(report)

    return report


def get_top_users(events: List[AuditEvent], limit: int = 10) -> List[Dict[str, Any]]:
    """Get top users by login count."""
    user_counts = {}
    for event in events:
        if event.user_id:
            user_counts[event.user_id] = user_counts.get(event.user_id, 0) + 1

    sorted_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)

    return [
        {
            "user_id": user_id,
            "login_count": count,
            "provider": get_user_provider(events, user_id),
        }
        for user_id, count in sorted_users[:limit]
    ]


def get_user_provider(events: List[AuditEvent], user_id: str) -> str:
    """Get most common provider for a user."""
    providers = {}
    for event in events:
        if event.user_id == user_id and event.provider:
            providers[event.provider] = providers.get(event.provider, 0) + 1

    if providers:
        return max(providers.items(), key=lambda x: x[1])[0]
    return "unknown"


def get_common_errors(events: List[AuditEvent], limit: int = 5) -> List[Dict[str, Any]]:
    """Get most common error messages."""
    error_counts = {}
    for event in events:
        if not event.success and event.error_message:
            error_counts[event.error_message] = (
                error_counts.get(event.error_message, 0) + 1
            )

    sorted_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)

    return [
        {"error_message": error, "count": count}
        for error, count in sorted_errors[:limit]
    ]


def get_provider_breakdown(events: List[AuditEvent]) -> Dict[str, Dict[str, Any]]:
    """Get detailed breakdown by provider."""
    breakdown = {}

    for event in events:
        provider = event.provider or "unknown"
        if provider not in breakdown:
            breakdown[provider] = {
                "total": 0,
                "successful": 0,
                "failed": 0,
                "unique_users": set(),
            }

        breakdown[provider]["total"] += 1
        if event.success:
            breakdown[provider]["successful"] += 1
        else:
            breakdown[provider]["failed"] += 1

        if event.user_id:
            breakdown[provider]["unique_users"].add(event.user_id)

    for provider in breakdown:
        breakdown[provider]["unique_users"] = len(breakdown[provider]["unique_users"])
        if breakdown[provider]["total"] > 0:
            breakdown[provider]["success_rate"] = (
                breakdown[provider]["successful"] / breakdown[provider]["total"]
            ) * 100
        else:
            breakdown[provider]["success_rate"] = 0

    return breakdown


def send_datadog_custom_metrics(report: Dict[str, Any]):
    """Send custom metrics to Datadog based on report."""
    tags = [
        f"report_type:{report['report_type']}",
        "service:federated_login",
        "env:" + os.getenv("ENVIRONMENT", "development"),
    ]

    statsd.gauge(
        "federated_login.report.total_users", len(report["top_users"]), tags=tags
    )
    statsd.gauge(
        "federated_login.report.unique_errors", len(report["common_errors"]), tags=tags
    )

    for provider, data in report["provider_breakdown"].items():
        provider_tags = tags + [f"provider:{provider}"]
        statsd.gauge(
            "federated_login.report.provider_success_rate",
            data.get("success_rate", 0),
            tags=provider_tags,
        )
