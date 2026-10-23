from __future__ import annotations

from typing import Any, Dict, List

from observability_client import (
    DatadogObservabilityClient,
    build_field_query,
    iso_utc_minutes_ago,
    iso_utc_now,
)
from observability_models import LogQuery


def fetch_recent_logs(
    field_filters: Dict[str, Any], minutes: int = 15, limit: int = 100
) -> List[Dict[str, Any]]:
    client = DatadogObservabilityClient()
    query = LogQuery(
        query=build_field_query(field_filters),
        from_time=iso_utc_minutes_ago(minutes),
        to_time=iso_utc_now(),
        limit=limit,
    )
    response = client.search_logs(query)
    return [
        {
            "timestamp": record.timestamp,
            "message": record.message,
            "service": record.service,
            "status": record.status,
            "attributes": record.attributes,
        }
        for record in response.records
    ]
