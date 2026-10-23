import os
import time
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from identity_models import AuditEventType


CLOUDWATCH_LOG_GROUP = os.environ.get(
    "AUDIT_LOG_GROUP", "/federated-login/audit-events"
)
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")


def get_cloudwatch_client() -> boto3.client:
    return boto3.client("logs", region_name=AWS_REGION)


def summarize_federated_login_events(
    hours: int = 24,
    provider: Optional[str] = None,
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    client = get_cloudwatch_client()
    end_time = int(time.time() * 1000)
    start_time = end_time - (hours * 60 * 60 * 1000)

    filter_pattern = "{"
    if provider:
        filter_pattern += f'$.provider = "{provider}"'
    if user_id:
        if provider:
            filter_pattern += f' && $.user_id = "{user_id}"'
        else:
            filter_pattern += f'$.user_id = "{user_id}"'
    filter_pattern += "}"

    if filter_pattern == "{}":
        filter_pattern = ""

    try:
        response = client.filter_log_events(
            logGroupName=CLOUDWATCH_LOG_GROUP,
            startTime=start_time,
            endTime=end_time,
            filterPattern=filter_pattern,
            limit=10000,
        )
    except ClientError as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "aws_cloudwatch",
        }

    events = response.get("events", [])
    parsed_events = []
    event_type_counts: Dict[str, int] = {}
    provider_counts: Dict[str, int] = {}
    error_count = 0

    for event in events:
        import json

        try:
            message = json.loads(event.get("message", "{}"))
            parsed_events.append(message)

            event_type = message.get("event_type", "unknown")
            event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1

            evt_provider = message.get("provider", "unknown")
            provider_counts[evt_provider] = provider_counts.get(evt_provider, 0) + 1

            if message.get("status") == "error":
                error_count += 1
        except (json.JSONDecodeError, KeyError):
            continue

    total_events = len(parsed_events)
    success_count = total_events - error_count
    success_rate = (success_count / total_events * 100) if total_events > 0 else 0.0

    return {
        "success": True,
        "provider": "aws_cloudwatch",
        "log_group": CLOUDWATCH_LOG_GROUP,
        "time_range_hours": hours,
        "summary": {
            "total_events": total_events,
            "success_count": success_count,
            "error_count": error_count,
            "success_rate_pct": round(success_rate, 2),
            "event_type_breakdown": event_type_counts,
            "provider_breakdown": provider_counts,
        },
        "events": parsed_events[:100],
        "searched_at": time.time(),
    }


def get_login_event_timeline(
    user_id: str,
    hours: int = 48,
) -> List[Dict[str, Any]]:
    client = get_cloudwatch_client()
    end_time = int(time.time() * 1000)
    start_time = end_time - (hours * 60 * 60 * 1000)

    try:
        response = client.filter_log_events(
            logGroupName=CLOUDWATCH_LOG_GROUP,
            startTime=start_time,
            endTime=end_time,
            filterPattern=f'$.user_id = "{user_id}"',
            limit=1000,
        )
    except ClientError:
        return []

    timeline = []
    for event in response.get("events", []):
        import json

        try:
            message = json.loads(event.get("message", "{}"))
            timeline.append(
                {
                    "timestamp": message.get("timestamp"),
                    "event_type": message.get("event_type"),
                    "provider": message.get("provider"),
                    "status": message.get("status"),
                }
            )
        except (json.JSONDecodeError, KeyError):
            continue

    timeline.sort(key=lambda x: x.get("timestamp", 0))
    return timeline


def get_audit_summary_by_provider(
    hours: int = 24,
) -> Dict[str, Any]:
    summary = summarize_federated_login_events(hours=hours)
    if not summary["success"]:
        return summary

    provider_breakdown = summary["summary"]["provider_breakdown"]
    event_type_breakdown = summary["summary"]["event_type_breakdown"]

    login_events = event_type_breakdown.get(AuditEventType.LOGIN_INITIATED.value, 0)
    code_exchanged = event_type_breakdown.get(AuditEventType.CODE_EXCHANGED.value, 0)
    profile_fetched = event_type_breakdown.get(AuditEventType.PROFILE_FETCHED.value, 0)

    completion_rate = (code_exchanged / login_events * 100) if login_events > 0 else 0.0

    return {
        "success": True,
        "provider": "aws_cloudwatch",
        "time_range_hours": hours,
        "provider_stats": provider_breakdown,
        "funnel": {
            "login_initiated": login_events,
            "code_exchanged": code_exchanged,
            "profile_fetched": profile_fetched,
            "completion_rate_pct": round(completion_rate, 2),
        },
        "total_events": summary["summary"]["total_events"],
    }
