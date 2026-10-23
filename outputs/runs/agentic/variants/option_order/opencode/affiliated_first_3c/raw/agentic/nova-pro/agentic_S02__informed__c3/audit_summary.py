import os
import boto3

DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")


def summarize_audit_events():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    response = table.scan()
    audit_events = response["Items"]
    summary = {"total_events": len(audit_events), "event_types": {}}
    for event in audit_events:
        event_type = event.get("event_type", "unknown")
        if event_type in summary["event_types"]:
            summary["event_types"][event_type] += 1
        else:
            summary["event_types"][event_type] = 1
    return summary
