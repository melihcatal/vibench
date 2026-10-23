from __future__ import annotations

from typing import Dict, Optional

from observability_client import DatadogObservabilityClient, build_search_payload


def fetch_recent_logs(
    service: str,
    start: str,
    end: str,
    field_filters: Optional[Dict[str, str]] = None,
    limit: int = 50,
) -> dict:
    client = DatadogObservabilityClient()
    terms = [f"service:{service}"]
    for key, value in (field_filters or {}).items():
        terms.append(f"@{key}:{value}")
    payload = build_search_payload(filter_query=" ".join(terms), start=start, end=end, limit=limit)
    return client.search_logs(payload).to_dict()
