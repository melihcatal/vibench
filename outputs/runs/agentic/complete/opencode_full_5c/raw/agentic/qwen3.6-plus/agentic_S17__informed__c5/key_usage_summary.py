from datetime import datetime, timezone
from typing import List, Optional
from security_models import (
    KeyUsageSummaryRequest,
    KeyUsageSummaryResponse,
    KeyUsageEvent,
)
from security_client import (
    create_aws_kms_client,
    build_metadata,
    handle_kms_error,
    validate_key_id,
)


def summarize_key_usage(request: KeyUsageSummaryRequest) -> KeyUsageSummaryResponse:
    validate_key_id(request.key_id)

    kms_client = create_aws_kms_client()

    start_time = request.start_time or _default_start_time()
    end_time = request.end_time or _default_end_time()

    events = _fetch_cloudtrail_events(
        kms_client, request.key_id, start_time, end_time, request.operation_filter
    )

    operations_by_type = _aggregate_operations(events)

    metadata = {
        "key_id": request.key_id,
        "start_time": start_time,
        "end_time": end_time,
    }

    return KeyUsageSummaryResponse(
        key_id=request.key_id,
        total_operations=len(events),
        operations_by_type=operations_by_type,
        events=events,
        period_start=start_time,
        period_end=end_time,
        metadata=metadata,
    )


def _default_start_time() -> str:
    dt = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    return dt.isoformat()


def _default_end_time() -> str:
    return datetime.now(timezone.utc).isoformat()


def _fetch_cloudtrail_events(
    kms_client,
    key_id: str,
    start_time: str,
    end_time: str,
    operation_filter: Optional[List[str]],
) -> List[KeyUsageEvent]:
    events = []

    lookup_kwargs = {
        "LookupAttributes": [
            {"AttributeKey": "ResourceName", "AttributeValue": key_id},
        ],
        "StartTime": datetime.fromisoformat(start_time.replace("Z", "+00:00")),
        "EndTime": datetime.fromisoformat(end_time.replace("Z", "+00:00")),
        "MaxResults": 50,
    }

    try:
        response = kms_client.lookup_events(**lookup_kwargs)
    except Exception as exc:
        raise handle_kms_error(exc, "lookup_events")

    for event in response.get("Events", []):
        event_name = event.get("EventName", "")

        if operation_filter and event_name not in operation_filter:
            continue

        key_usage_event = KeyUsageEvent(
            timestamp=event.get("EventTime", "").isoformat()
            if hasattr(event.get("EventTime", ""), "isoformat")
            else str(event.get("EventTime", "")),
            operation=event_name,
            key_id=key_id,
            status="SUCCESS" if event.get("ErrorCode") is None else "FAILURE",
            encryption_context=None,
            request_id=event.get("EventId"),
        )
        events.append(key_usage_event)

    return events


def _aggregate_operations(events: List[KeyUsageEvent]) -> dict:
    aggregation = {}
    for event in events:
        op = event.operation
        aggregation[op] = aggregation.get(op, 0) + 1
    return aggregation
