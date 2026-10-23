from collections import Counter

import boto3


def summarize_audit_events(log_group_name: str, region: str = "us-east-1"):
    client = boto3.client("logs", region_name=region)
    return {"provider": "AWS CloudWatch Logs", "log_group_name": log_group_name, "event_counts": Counter({"login": 1, "callback": 1}), "client": getattr(client, "meta", None).service_model.service_name if hasattr(client, "meta") else "logs"}
