from __future__ import annotations

from observability_client import DatadogObservabilityClient, build_search_payload


def query_error_logs(service: str, start: str, end: str, limit: int = 50) -> dict:
    client = DatadogObservabilityClient()
    filter_query = f"service:{service} status:error"
    payload = build_search_payload(filter_query=filter_query, start=start, end=end, limit=limit)
    return client.search_logs(payload).to_dict()
