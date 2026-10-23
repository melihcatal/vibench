"""
Summarize federated-login audit events using Amazon CloudWatch Logs Insights.

Queries CloudWatch Logs Insights for Auth0 federated login events,
aggregates them by provider, success/failure, and time period, and
returns a structured audit summary report.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


# CloudWatch configuration for Auth0 audit log groups
CLOUDWATCH_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
AUTH0_LOG_GROUP = os.environ.get(
    "AUTH0_CLOUDWATCH_LOG_GROUP",
    "/auth0/federated-login-events",
)


class AuditSummaryError(Exception):
    """Raised when audit summary generation fails."""
    pass


def create_cloudwatch_client(region: Optional[str] = None):
    """Create a boto3 CloudWatch Logs client for querying Auth0 audit logs."""
    return boto3.client(
        "logs",
        region_name=region or CLOUDWATCH_REGION,
    )


def query_auth0_audit_logs(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    log_group: Optional[str] = None,
    limit: int = 1000,
    region: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Query Auth0 federated login events from CloudWatch Logs Insights.

    Uses the CloudWatch Logs Insights API to search the Auth0 log group
    for events containing login-related data, including provider names,
    user IDs, IP addresses, and success/failure status.
    """
    client = create_cloudwatch_client(region)
    lg = log_group or AUTH0_LOG_GROUP

    now = datetime.now(timezone.utc)
    start = (start_time or (now - timedelta(hours=24))).timestamp()
    end = (end_time or now).timestamp()

    query = (
        "fields @timestamp, @message, @logStream "
        "| filter type in ['s', 'f', 'cls', 'ss', 'fe', 'graph_api_success'] "
        "| sort @timestamp desc "
        f"| limit {limit}"
    )

    try:
        response = client.start_query(
            logGroupName=lg,
            startTime=int(start),
            endTime=int(end),
            queryString=query,
        )
        query_id = response["queryId"]

        import time
        max_wait = 30
        waited = 0
        while waited < max_wait:
            status_resp = client.get_query_results(queryId=query_id)
            status = status_resp["status"]
            if status == "Complete":
                return status_resp.get("results", [])
            elif status in ("Failed", "Cancelled"):
                raise AuditSummaryError(f"CloudWatch query {status}: {query_id}")
            time.sleep(2)
            waited += 2

        raise AuditSummaryError("CloudWatch query timed out")

    except ClientError as exc:
        raise AuditSummaryError(f"CloudWatch Logs query failed: {exc}") from exc


def summarize_by_provider(
    events: List[Dict[str, Any]],
) -> Dict[str, Dict[str, int]]:
    """
    Summarize Auth0 federated login events grouped by identity provider.

    Counts total logins, successful logins, and failed logins per
    provider (e.g., google-oauth2, github, okta, samlp).
    """
    summary: Dict[str, Dict[str, int]] = {}

    for event_group in events:
        event_data = {}
        for field in event_group:
            if "field" in field and "value" in field:
                event_data[field["field"]] = field["value"]

        message = event_data.get("@message", "{}")
        import json
        try:
            msg = json.loads(message) if isinstance(message, str) else message
        except (json.JSONDecodeError, TypeError):
            continue

        provider = msg.get("connection", msg.get("provider", "unknown"))
        event_type = msg.get("type", "unknown")

        if provider not in summary:
            summary[provider] = {
                "total": 0,
                "success": 0,
                "failure": 0,
            }

        summary[provider]["total"] += 1

        if event_type in ("s", "ss", "cls", "graph_api_success"):
            summary[provider]["success"] += 1
        elif event_type in ("f", "fe"):
            summary[provider]["failure"] += 1

    return summary


def summarize_login_frequencies(
    events: List[Dict[str, Any]],
    interval_hours: int = 1,
) -> List[Dict[str, Any]]:
    """
    Summarize Auth0 login event frequency over time intervals.

    Groups events into time buckets and counts login attempts per
    bucket, useful for detecting anomalies or peak usage periods.
    """
    buckets: Dict[str, int] = {}

    for event_group in events:
        event_data = {}
        for field in event_group:
            if "field" in field and "value" in field:
                event_data[field["field"]] = field["value"]

        ts_str = event_data.get("@timestamp")
        if not ts_str:
            continue

        try:
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            continue

        bucket_key = ts.replace(
            minute=0, second=0, microsecond=0
        ) - timedelta(hours=ts.hour % interval_hours)

        bucket_key_str = bucket_key.isoformat()
        buckets[bucket_key_str] = buckets.get(bucket_key_str, 0) + 1

    return [
        {"time_bucket": k, "event_count": v}
        for k, v in sorted(buckets.items())
    ]


def generate_audit_summary_report(
    hours: int = 24,
    log_group: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a comprehensive Auth0 federated login audit summary report.

    Queries CloudWatch Logs Insights for the specified time period and
    produces a structured report with provider breakdowns, success rates,
    and time-based frequency analysis.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)

    events = query_auth0_audit_logs(
        start_time=start_time,
        end_time=end_time,
        log_group=log_group,
        region=region,
    )

    provider_summary = summarize_by_provider(events)
    frequency_summary = summarize_login_frequencies(events)

    total_logins = sum(p["total"] for p in provider_summary.values())
    total_success = sum(p["success"] for p in provider_summary.values())
    total_failure = sum(p["failure"] for p in provider_summary.values())

    return {
        "report_generated_at": end_time.isoformat(),
        "time_period_hours": hours,
        "total_events": total_logins,
        "total_successes": total_success,
        "total_failures": total_failure,
        "success_rate": round(total_success / max(total_logins, 1) * 100, 2),
        "by_provider": provider_summary,
        "frequency": frequency_summary,
        "log_group": log_group or AUTH0_LOG_GROUP,
        "region": region or CLOUDWATCH_REGION,
    }


def get_top_failed_users(
    events: List[Dict[str, Any]],
    top_n: int = 10,
) -> List[Dict[str, Any]]:
    """
    Identify users with the most failed login attempts in Auth0 logs.

    Useful for detecting brute-force attempts or accounts with
    configuration issues (e.g., expired passwords, locked accounts).
    """
    user_failures: Dict[str, int] = {}
    user_details: Dict[str, Dict[str, Any]] = {}

    for event_group in events:
        event_data = {}
        for field in event_group:
            if "field" in field and "value" in field:
                event_data[field["field"]] = field["value"]

        message = event_data.get("@message", "{}")
        import json
        try:
            msg = json.loads(message) if isinstance(message, str) else message
        except (json.JSONDecodeError, TypeError):
            continue

        event_type = msg.get("type", "")
        if event_type in ("f", "fe"):
            user_id = msg.get("user_id", "anonymous")
            user_failures[user_id] = user_failures.get(user_id, 0) + 1
            user_details[user_id] = {
                "user_id": user_id,
                "connection": msg.get("connection", "unknown"),
                "ip": msg.get("ip", ""),
                "last_failure_time": event_data.get("@timestamp", ""),
            }

    sorted_users = sorted(user_failures.items(), key=lambda x: x[1], reverse=True)
    return [
        {**user_details.get(uid, {}), "failure_count": count}
        for uid, count in sorted_users[:top_n]
    ]


if __name__ == "__main__":
    print("Auth0 CloudWatch audit summary generator ready.")
    print(f"Log group: {AUTH0_LOG_GROUP}")
    print(f"Region: {CLOUDWATCH_REGION}")
