from __future__ import annotations

import boto3

from security_models import AuditSummary


def key_usage_summary(key_id: str) -> AuditSummary:
    cloudtrail = boto3.client("cloudtrail")
    response = cloudtrail.lookup_events(LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": key_id}])
    operations: dict[str, int] = {}
    for event in response.get("Events", []):
        name = event.get("EventName", "unknown")
        operations[name] = operations.get(name, 0) + 1
    return AuditSummary(key_id=key_id, operations=operations, notes="AWS CloudTrail key usage summary")
