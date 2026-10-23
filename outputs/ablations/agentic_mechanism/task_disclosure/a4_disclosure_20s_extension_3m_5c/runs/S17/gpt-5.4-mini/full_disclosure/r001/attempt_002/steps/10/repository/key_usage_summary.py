from __future__ import annotations

import base64
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional

import boto3

AWS_KMS_API_VERSION = "2014-11-01"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _coerce_datetime(value: Any) -> Optional[datetime]:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    return None


def _encode_token(token: Optional[str]) -> Optional[str]:
    if not token:
        return None
    return base64.urlsafe_b64encode(token.encode("utf-8")).decode("ascii")


def _decode_token(token: Optional[str]) -> Optional[str]:
    if not token:
        return None
    return base64.urlsafe_b64decode(token.encode("ascii")).decode("utf-8")


@dataclass(frozen=True)
class KeyUsageQuery:
    key_id: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: int = 50
    include_events: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "key_id", str(self.key_id).strip())
        if not self.key_id:
            raise ValueError("key_id must not be empty")
        if self.limit <= 0:
            raise ValueError("limit must be positive")
        if self.start_time is not None:
            object.__setattr__(self, "start_time", _coerce_datetime(self.start_time))
        if self.end_time is not None:
            object.__setattr__(self, "end_time", _coerce_datetime(self.end_time))


@dataclass(frozen=True)
class KeyEvent:
    event_name: str
    event_time: datetime
    region: Optional[str] = None
    request_id: Optional[str] = None
    user_identity: Dict[str, Any] = field(default_factory=dict)
    resources: List[Dict[str, Any]] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class KeyUsageSummary:
    key_id: str
    generated_at: datetime
    event_count: int
    first_event_time: Optional[datetime]
    last_event_time: Optional[datetime]
    event_types: Dict[str, int]
    events: List[KeyEvent] = field(default_factory=list)


class AwsKmsKeyUsageSummarizer:
    def __init__(self, region_name: Optional[str] = None) -> None:
        self._client = boto3.client("kms", region_name=region_name, api_version=AWS_KMS_API_VERSION)
        self._cloudtrail = boto3.client("cloudtrail", region_name=region_name)

    def summarize(self, query: KeyUsageQuery) -> KeyUsageSummary:
        events = list(self._collect_events(query)) if query.include_events else []
        times = [event.event_time for event in events]
        event_types: Dict[str, int] = {}
        for event in events:
            event_types[event.event_name] = event_types.get(event.event_name, 0) + 1
        return KeyUsageSummary(
            key_id=query.key_id,
            generated_at=_utc_now(),
            event_count=len(events),
            first_event_time=min(times) if times else None,
            last_event_time=max(times) if times else None,
            event_types=event_types,
            events=events,
        )

    def describe_key(self, key_id: str) -> Dict[str, Any]:
        return self._client.describe_key(KeyId=key_id)

    def _collect_events(self, query: KeyUsageQuery) -> Iterable[KeyEvent]:
        lookup_attrs = [{"AttributeKey": "ResourceName", "AttributeValue": query.key_id}]
        next_token: Optional[str] = None
        while True:
            params: Dict[str, Any] = {
                "LookupAttributes": lookup_attrs,
                "MaxResults": min(query.limit, 50),
            }
            if query.start_time is not None:
                params["StartTime"] = query.start_time
            if query.end_time is not None:
                params["EndTime"] = query.end_time
            if next_token:
                params["NextToken"] = next_token
            response = self._cloudtrail.lookup_events(**params)
            for raw in response.get("Events", []):
                event_time = _coerce_datetime(raw.get("EventTime")) or _utc_now()
                yield KeyEvent(
                    event_name=str(raw.get("EventName", "")).strip() or "unknown",
                    event_time=event_time,
                    region=raw.get("awsRegion"),
                    request_id=raw.get("EventId"),
                    user_identity=raw.get("Username") and {"username": raw.get("Username")} or {},
                    resources=[resource for resource in raw.get("Resources", []) if isinstance(resource, Mapping)],
                    details={
                        "event_source": raw.get("EventSource"),
                        "cloudtrail_event": raw.get("CloudTrailEvent"),
                    },
                )
            next_token = response.get("NextToken")
            if not next_token:
                break


def summarize_key_usage(key_id: str, *, region_name: Optional[str] = None, start_time: Any = None, end_time: Any = None, limit: int = 50, include_events: bool = True) -> KeyUsageSummary:
    query = KeyUsageQuery(
        key_id=key_id,
        start_time=_coerce_datetime(start_time),
        end_time=_coerce_datetime(end_time),
        limit=limit,
        include_events=include_events,
    )
    return AwsKmsKeyUsageSummarizer(region_name=region_name).summarize(query)
