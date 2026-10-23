from __future__ import annotations

from typing import Dict, List

import boto3

from security_models import AuditRecord, KeyOperationResponse


AWS_CLOUDTRAIL_PROVIDER = "boto3:cloudtrail"


def key_usage_summary(key_id: str, region: str = "us-east-1") -> KeyOperationResponse:
    client = boto3.client("cloudtrail", region_name=region)
    events = client.lookup_events(LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": key_id}])
    records: List[AuditRecord] = []
    for event in events.get("Events", []):
        records.append(AuditRecord(subject=key_id, action=event.get("EventName", "unknown"), details={"event_id": event.get("EventId")}))
    summary: Dict[str, int] = {}
    for record in records:
        summary[record.action] = summary.get(record.action, 0) + 1
    return KeyOperationResponse(key_id=key_id, result=str(summary), metadata={"provider": AWS_CLOUDTRAIL_PROVIDER, "events": len(records)})
