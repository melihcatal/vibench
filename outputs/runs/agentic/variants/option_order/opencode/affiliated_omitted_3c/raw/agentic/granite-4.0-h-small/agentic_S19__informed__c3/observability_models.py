# Define local request, response, and normalization helpers for Managed Metrics Monitoring using Datadog

import json
from typing import Any, Dict
from .observability_client import api_client

METRIC_NAME = "example.metric"
TIME_WINDOW = "last_5m"

# ---------------------------------------------------------------------------
# Request helpers
# ---------------------------------------------------------------------------


def request_metric_window(params: Dict[str, Any] = {}) -> Dict[str, Any]:
    """Build and send a query for recent metric points over a time window."""
    payload = {
        "from": "now-{0}".format(params.get("window", TIME_WINDOW)),
        "to": "now",
        "query": f"{METRIC_NAME}".strip(),
    }
    return payload


# ---------------------------------------------------------------------------
# Response helpers
# ---------------------------------------------------------------------------


def normalize_datadog_points(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize Datadog's metric response into a generic structure."""
    data = {}
    for series in raw.get("series", []):
        # keep only the values and timestamps for generic use
        data[series.get("metric", "")] = [
            {"timestamp": v["timestamp"], "value": v["value"]}
            for v in series.get("points", [])
        ]
    return data


# ---------------------------------------------------------------------------
# Example usage entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cfg = api_client()
    resp = cfg.get_metrics(query=METRIC_NAME, from_="now-5m", to="now")
    print(json.dumps(normalize_datadog_points(resp), indent=2))
