import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import boto3


@dataclass
class KeyUsageSummary:
    key_id: str
    total_events: int
    event_types: Dict[str, int]
    last_event_at: Optional[str]
    window_start: str
    window_end: str
    account_id: Optional[str] = None
    region: Optional[str] = None


def _isoformat(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _parse_time(value: Any) -> Optional[datetime]:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc)
    if isinstance(value, str):
        try:
            if value.endswith("Z"):
                value = value[:-1] + "+00:00"
            return datetime.fromisoformat(value).astimezone(timezone.utc)
        except ValueError:
            return None
    return None


def _extract_event_time(event: Dict[str, Any]) -> Optional[datetime]:
    for key in ("eventTime", "time", "timestamp", "createdAt"):
        dt = _parse_time(event.get(key))
        if dt:
            return dt
    return None


def summarize_key_usage(key_id: str, days: int = 30, region: Optional[str] = None) -> KeyUsageSummary:
    region_name = region or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    session = boto3.Session(region_name=region_name)
    sts = session.client("sts")
    kms = session.client("kms")
    cloudtrail = session.client("cloudtrail")

    identity = sts.get_caller_identity()
    account_id = identity.get("Account")

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=days)

    event_types: Dict[str, int] = {}
    events: List[Dict[str, Any]] = []

    token: Optional[str] = None
    while True:
        params: Dict[str, Any] = {
            "LookupAttributes": [
                {"AttributeKey": "ResourceName", "AttributeValue": key_id},
            ],
            "StartTime": start_time,
            "EndTime": end_time,
            "MaxResults": 50,
        }
        if token:
            params["NextToken"] = token
        response = cloudtrail.lookup_events(**params)
        batch = response.get("Events", [])
        events.extend(batch)
        token = response.get("NextToken")
        if not token:
            break

    last_event_time: Optional[datetime] = None
    for event in events:
        event_name = event.get("EventName") or event.get("eventName") or "unknown"
        event_types[event_name] = event_types.get(event_name, 0) + 1
        event_time = _extract_event_time(event)
        if event_time and (last_event_time is None or event_time > last_event_time):
            last_event_time = event_time

    try:
        kms.describe_key(KeyId=key_id)
    except Exception:
        pass

    return KeyUsageSummary(
        key_id=key_id,
        total_events=len(events),
        event_types=dict(sorted(event_types.items())),
        last_event_at=_isoformat(last_event_time) if last_event_time else None,
        window_start=_isoformat(start_time),
        window_end=_isoformat(end_time),
        account_id=account_id,
        region=region_name,
    )


def summarize_key_usage_as_dict(key_id: str, days: int = 30, region: Optional[str] = None) -> Dict[str, Any]:
    summary = summarize_key_usage(key_id=key_id, days=days, region=region)
    return {
        "key_id": summary.key_id,
        "total_events": summary.total_events,
        "event_types": summary.event_types,
        "last_event_at": summary.last_event_at,
        "window_start": summary.window_start,
        "window_end": summary.window_end,
        "account_id": summary.account_id,
        "region": summary.region,
    }
