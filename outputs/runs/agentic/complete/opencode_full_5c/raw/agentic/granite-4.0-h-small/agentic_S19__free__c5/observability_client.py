# [HELPER] observability_client.py

# Local configuration and client helper utilities for Managed Metrics Monitoring.
# This module provides thin wrappers around a concrete provider's SDK (New Relic in this case)
# to abstract authentication, request building, and error handling.

import os
from datetime import datetime
import json
from typing import Any, Dict

# Import the official New Relic Python SDK (newrelic-api).
# The package name reflects the concrete provider.
import newrelic_api


class NewRelicClient:
    """Thin wrapper around New Relic's API client that handles auth and common patterns.

    - Reads API key from environment variable NR_API_KEY.
    - Exposes high‑level methods matching the scored file signatures.
    """

    def __init__(self) -> None:
        api_key = os.getenv("NR_API_KEY")
        if not api_key:
            raise RuntimeError(
                "New Relic API key not found in environment variable NR_API_KEY"
            )
        newrelic_api.set_api_key(api_key)

    def _build_payload(self, **kwargs: Any) -> Dict[str, Any]:
        """Create a JSON‑serializable payload from keyword arguments."""
        return {k: v for k, v in kwargs.items() if v is not None}

    def query_metrics(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Query raw datapoints using New Relic Insights NRDB syntax."""
        query = (
            "SELECT * FROM Metric WHERE metricName = :metricName"
            " SINCE :start UNLESS SINCE :end LIMIT :limit"
        )
        variables = {
            "metricName": payload["metric"],
            "start": payload["start"],
            "end": payload["end"],
            "limit": payload["limit"],
        }
        # Execute the NRDB query via the SDK client.
        result = newrelic_api.nrdb_query(query=query, variables=variables)
        return (
            result.json()
        )  # Returns a Python dict representation of the JSON response.

    def get_stats(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Get aggregated statistics for a metric."""
        query = (
            "SELECT average(duration), min(duration), max(duration), sum(duration), count(*)"
            " FROM Metric WHERE metricName = :metricName"
            " SINCE :start UNLESS SINCE :end"
        )
        variables = {
            "metricName": payload["metric"],
            "start": payload["start"],
            "end": payload["end"],
        }
        result = newrelic_api.nrdb_query(query=query, variables=variables)
        return result.json()

    def query_filtered_metrics(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Query metrics with dimension filters."""
        query = (
            "SELECT * FROM Metric WHERE metricName = :metricName"
            " AND host IN (:hosts)"
            " SINCE :start UNLESS SINCE :end"
        )
        variables = {
            "metricName": payload["metric"],
            "hosts": payload["dimensions"].get("host", []),
            "start": payload["start"],
            "end": payload["end"],
        }
        result = newrelic_api.nrdb_query(query=query, variables=variables)
        return result.json()

    def compare_series(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Compare two filtered series of the same metric."""
        query = (
            "SELECT average(duration) FROM Metric WHERE metricName = :metricName"
            " AND host = :host_left SINCE :start"
            " COMPARE WITH average(duration) FROM Metric WHERE metricName = :metricName"
            " AND host = :host_right SINCE :start"
        )
        variables = {
            "metricName": payload["metric"],
            "host_left": next(iter(payload["left_filter"].get("host", []))),
            "host_right": next(iter(payload["right_filter"].get("host", []))),
            "start": payload["start"],
            "end": payload["end"],
        }
        result = newrelic_api.nrdb_query(query=query, variables=variables)
        return result.json()

    def _normalize_response(self, raw: Dict[str, Any]) -> Any:
        """Placeholder for normalization logic that converts provider specific schema to internal models."""
        # In a real implementation, map raw keys to observability_models structures.
        return raw


if __name__ == "__main__":
    client = NewRelicClient()
    # Simple smoke test to verify the client works (will raise if NR_API_KEY missing).
    print("Client initialized successfully with API key present.")
