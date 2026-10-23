import json
import datetime
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Audit summary / reporting utilities

dynamo = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION", "us-east-1"))
TABLE_NAME = os.getenv("AUDIT_TABLE_NAME", "federated-login-audit")


def summarize_audit_range(start_ts: str, end_ts: str) -> dict:
    """Return a summary of audit events between two ISO timestamps.
    Args:
        start_ts (str): ISO8601 start (inclusive).
        end_ts (str): ISO8601 end (inclusive).
    Returns:
        dict: Counts per event_type and per provider.
    """
    table = dynamo.Table(TABLE_NAME)
    try:
        response = table.scan(
            FilterExpression=Attr("event_timestamp").between(start_ts, end_ts)
        )
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Audit query failed: {e}")
    events = response.get("Items", [])
    summary = {"total_events": len(events), "by_type": {}, "by_provider": {}}
    for ev in events:
        et = ev.get("event_type", "unknown")
        pt = ev.get("provider", "unknown")
        summary["by_type"][et] = summary["by_type"].get(et, 0) + 1
        summary["by_provider"][pt] = summary["by_provider"].get(pt, 0) + 1
    return summary


# Example usage (for local testing):
# start = (datetime.datetime.utcnow() - datetime.timedelta(minutes=30)).isoformat() + "Z"
# end = datetime.datetime.utcnow().isoformat() + "Z"
# print(summarize_audit_range(start, end))
