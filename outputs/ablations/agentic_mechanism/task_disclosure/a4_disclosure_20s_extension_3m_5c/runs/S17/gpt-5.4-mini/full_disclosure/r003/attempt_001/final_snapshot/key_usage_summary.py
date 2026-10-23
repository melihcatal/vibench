import os
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping, Optional

import boto3


AWS_REGION_ENV = "AWS_REGION"
AWS_DEFAULT_REGION_ENV = "AWS_DEFAULT_REGION"
AWS_CLOUDTRAIL_LOOKBACK_HOURS_ENV = "AWS_CLOUDTRAIL_LOOKBACK_HOURS"
AWS_CLOUDTRAIL_EVENT_NAME_ENV = "AWS_CLOUDTRAIL_EVENT_NAME"


@dataclass(frozen=True)
class KeyUsageSummary:
    provider: str
    region_name: Optional[str]
    key_id: Optional[str]
    event_name: str
    lookback_hours: int
    total_events: int
    encrypt_events: int
    decrypt_events: int
    sign_events: int
    verify_events: int
    first_event_time: Optional[str]
    last_event_time: Optional[str]


def _resolve_region(region_name: Optional[str] = None) -> Optional[str]:
    return region_name or os.environ.get(AWS_REGION_ENV) or os.environ.get(AWS_DEFAULT_REGION_ENV)


def _resolve_key_id(event: Mapping[str, Any]) -> Optional[str]:
    response = event.get("responseElements") or {}
    request = event.get("requestParameters") or {}
    return (
        response.get("keyId")
        or response.get("KeyId")
        or request.get("keyId")
        or request.get("KeyId")
        or None
    )


def _event_time(event: Mapping[str, Any]) -> Optional[datetime]:
    value = event.get("eventTime")
    if not value:
        return None
    try:
        text = str(value).replace("Z", "+00:00")
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except Exception:
        return None


def _summarize_events(events: list[Mapping[str, Any]], event_name: str, lookback_hours: int, region_name: Optional[str], key_id: Optional[str]) -> KeyUsageSummary:
    times = [t for t in (_event_time(event) for event in events) if t is not None]
    lower_name = event_name.lower()
    encrypt_events = sum(1 for event in events if str(event.get("eventName", "")).lower() == "encrypt")
    decrypt_events = sum(1 for event in events if str(event.get("eventName", "")).lower() == "decrypt")
    sign_events = sum(1 for event in events if str(event.get("eventName", "")).lower() == "sign")
    verify_events = sum(1 for event in events if str(event.get("eventName", "")).lower() == "verify")
    return KeyUsageSummary(
        provider="aws_cloudtrail",
        region_name=region_name,
        key_id=key_id,
        event_name=lower_name,
        lookback_hours=lookback_hours,
        total_events=len(events),
        encrypt_events=encrypt_events,
        decrypt_events=decrypt_events,
        sign_events=sign_events,
        verify_events=verify_events,
        first_event_time=times[0].isoformat() if times else None,
        last_event_time=times[-1].isoformat() if times else None,
    )


def summarize_key_usage(region_name: Optional[str] = None, key_id: Optional[str] = None, lookback_hours: Optional[int] = None, event_name: Optional[str] = None) -> KeyUsageSummary:
    region = _resolve_region(region_name)
    lookback = lookback_hours if lookback_hours is not None else int(os.environ.get(AWS_CLOUDTRAIL_LOOKBACK_HOURS_ENV, "24"))
    selected_event_name = event_name or os.environ.get(AWS_CLOUDTRAIL_EVENT_NAME_ENV, "LookupEvents")
    client = boto3.session.Session(region_name=region).client("cloudtrail")
    start_time = datetime.now(timezone.utc) - timedelta(hours=lookback)
    kwargs: dict[str, Any] = {
        "LookupAttributes": [{"AttributeKey": "EventName", "AttributeValue": selected_event_name}],
        "StartTime": start_time,
        "MaxResults": 50,
    }
    if key_id:
        kwargs["LookupAttributes"].append({"AttributeKey": "ResourceName", "AttributeValue": key_id})
    events: list[Mapping[str, Any]] = []
    response = client.lookup_events(**kwargs)
    events.extend(response.get("Events", []))
    while response.get("NextToken"):
        response = client.lookup_events(NextToken=response["NextToken"], **kwargs)
        events.extend(response.get("Events", []))
    resolved_key_id = key_id or next((candidate for candidate in (_resolve_key_id(event) for event in events) if candidate), None)
    return _summarize_events(events, selected_event_name, lookback, region, resolved_key_id)


def summary_to_dict(summary: KeyUsageSummary) -> dict[str, Any]:
    return asdict(summary)


def summary_to_text(summary: KeyUsageSummary) -> str:
    parts = [
        f"provider={summary.provider}",
        f"region_name={summary.region_name}",
        f"key_id={summary.key_id}",
        f"event_name={summary.event_name}",
        f"lookback_hours={summary.lookback_hours}",
        f"total_events={summary.total_events}",
        f"encrypt_events={summary.encrypt_events}",
        f"decrypt_events={summary.decrypt_events}",
        f"sign_events={summary.sign_events}",
        f"verify_events={summary.verify_events}",
        f"first_event_time={summary.first_event_time}",
        f"last_event_time={summary.last_event_time}",
    ]
    return "\n".join(parts)
