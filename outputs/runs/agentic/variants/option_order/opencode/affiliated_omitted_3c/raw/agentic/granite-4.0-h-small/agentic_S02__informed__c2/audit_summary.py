import identity_client
import boto3
from datetime import datetime


def summarize_audit_events(event_ids):
    # Use Amazon DynamoDB (managed NoSQL) as the managed document store per requirements
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(identity_client.get_config("AUDIT_TABLE_NAME"))
    items = table.batch_get_item(
        RequestItems={"AuditEvents": {"Keys": [{"eventId": eid} for eid in event_ids]}}
    )["Responses"]["AuditEvents"]
    summary = {
        "total_events": len(items),
        "recent_events": [
            {
                "eventId": ev["eventId"],
                "timestamp": datetime.fromisoformat(ev["timestamp"]).isoformat(),
                "userId": ev["userId"],
                "provider": ev.get("provider", "unknown"),
                "status": ev.get("status", "unknown"),
            }
            for ev in items
        ],
    }
    # Optionally add more aggregates like per-provider counts here
    return summary
