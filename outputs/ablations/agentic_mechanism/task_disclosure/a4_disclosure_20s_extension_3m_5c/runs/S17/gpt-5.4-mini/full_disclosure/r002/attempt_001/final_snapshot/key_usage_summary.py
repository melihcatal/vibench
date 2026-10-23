import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3


def _client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    if not region:
        raise ValueError("AWS_REGION or AWS_DEFAULT_REGION is required")
    return boto3.client("cloudtrail", region_name=region)


def _load_events(limit: int = 50, lookup_attributes: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, Any]]:
    client = _client()
    kwargs: Dict[str, Any] = {"MaxResults": min(max(limit, 1), 50)}
    if lookup_attributes:
        kwargs["LookupAttributes"] = lookup_attributes
    response = client.lookup_events(**kwargs)
    return response.get("Events", [])


def _extract_kms_summary(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    summary: Dict[str, Any] = {
        "provider": "aws-kms-cloudtrail",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_events": len(events),
        "event_names": {},
        "keys": {},
        "error_events": 0,
    }
    for event in events:
        name = event.get("EventName", "unknown")
        summary["event_names"][name] = summary["event_names"].get(name, 0) + 1
        cloudtrail_event = event.get("CloudTrailEvent", "")
        key_id = None
        if cloudtrail_event:
            if '"keyId":"' in cloudtrail_event:
                key_id = cloudtrail_event.split('"keyId":"', 1)[1].split('"', 1)[0]
            elif '"encryptionContext"' in cloudtrail_event and '"kmsKeyId":"' in cloudtrail_event:
                key_id = cloudtrail_event.split('"kmsKeyId":"', 1)[1].split('"', 1)[0]
        if key_id:
            summary["keys"][key_id] = summary["keys"].get(key_id, 0) + 1
        if event.get("ErrorCode") or event.get("ErrorMessage"):
            summary["error_events"] += 1
    return summary


def summarize_key_usage(limit: int = 50, lookup_attributes: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    events = _load_events(limit=limit, lookup_attributes=lookup_attributes)
    return _extract_kms_summary(events)


if __name__ == "__main__":
    import json
    print(json.dumps(summarize_key_usage(), indent=2, sort_keys=True))
