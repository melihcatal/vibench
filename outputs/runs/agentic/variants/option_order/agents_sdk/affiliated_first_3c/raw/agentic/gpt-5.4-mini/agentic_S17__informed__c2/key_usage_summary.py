from __future__ import annotations

import os
from typing import Any, Dict, List

import boto3

AWS_SECURITY_SERVICE = "Amazon CloudWatch Logs"


def summarize_key_usage(log_group_name: str, limit: int = 50) -> Dict[str, Any]:
    client = boto3.client("logs", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    response = client.filter_log_events(
        logGroupName=log_group_name,
        limit=limit,
        filterPattern='"kms" OR "decrypt" OR "encrypt" OR "sign" OR "verify"',
    )
    events: List[Dict[str, Any]] = []
    for event in response.get("events", []):
        events.append(
            {
                "timestamp": event.get("timestamp"),
                "message": event.get("message"),
                "ingestionTime": event.get("ingestionTime"),
            }
        )
    return {
        "service": AWS_SECURITY_SERVICE,
        "log_group_name": log_group_name,
        "matched_events": len(events),
        "events": events,
    }
