import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from identity_models import AuditEvent
import boto3
from boto3.dynamodb.conditions import Key


def summarize_audit_events(user_id: str, days: int = 7) -> Dict[str, Any]:
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    table = dynamodb.Table("federated-login-audit")

    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    response = table.query(
        KeyConditionExpression=Key("user_id").eq(user_id)
        & Key("timestamp").between(start_date.isoformat(), end_date.isoformat())
    )

    events = response.get("Items", [])

    summary = {
        "user_id": user_id,
        "period_days": days,
        "total_events": len(events),
        "providers": {},
        "event_types": {},
        "first_event": None,
        "last_event": None,
    }

    for event in events:
        provider = event.get("provider", "unknown")
        event_type = event.get("event_type", "unknown")

        summary["providers"][provider] = summary["providers"].get(provider, 0) + 1
        summary["event_types"][event_type] = (
            summary["event_types"].get(event_type, 0) + 1
        )

        event_time = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
        if not summary["first_event"] or event_time < summary["first_event"]:
            summary["first_event"] = event_time.isoformat()
        if not summary["last_event"] or event_time > summary["last_event"]:
            summary["last_event"] = event_time.isoformat()

    return summary
