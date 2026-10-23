# metric_summary.py

from __future__ import annotations

import json
from typing import Any, Dict, List

from observability_client import get_metrics_client
from observability_models import RequestModel, DimensionFilter

# ---------------------------------------------------------------------------
# Configuration (choose ONE concrete provider)
# ---------------------------------------------------------------------------
# Example: IBM Cloud Monitoring
IBM_MONITORING_INSTANCE_ID = "YOUR_MONITORING_INSTANCE_ID"
IBM_CLOUD_API_KEY = "YOUR_IBM_CLOUD_API_KEY"

# Example: Amazon CloudWatch Metrics (uncomment if using AWS)
# AWS_ACCESS_KEY_ID = "YOUR_AWS_ACCESS_KEY_ID"
# AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"

# ---------------------------------------------------------------------------
# Helper: build payload for recent window (default last hour)
# ---------------------------------------------------------------------------


def build_recent_window_payload(
    metric_name: str, filters: List[DimensionFilter] = None
) -> RequestModel:
    """Create a request model covering the most recent hour."""
    now = int(time.time())
    hour_ago = now - 3600
    payload: RequestModel = {
        "metric": metric_name,
        "start": hour_ago,
        "end": now,
        "filters": filters or [],
    }
    return payload


# ---------------------------------------------------------------------------
# Core integration function
# ---------------------------------------------------------------------------


def metric_summary(
    metric_name: str, filters: List[DimensionFilter] = None
) -> Dict[str, Any]:
    """Summarize recent metric trends or anomalies.

    The function sends the payload to a hosted LLM inference service (e.g., watsonx.ai) to request a natural‑language summary.
    The response is returned verbatim for downstream consumption.
    """
    client = get_metrics_client()  # uses the configured provider
    payload = build_recent_window_payload(metric_name, filters)
    # Send request to hosted LLM inference (example uses watsonx.ai text generation)
    summary_response = client.query(
        payload={"task": "summarize", "metric": metric_name, "data": payload}
    )
    # In a real implementation this would call the specific provider's API; here we treat client.query as the abstraction.
    return {
        "metric": metric_name,
        "summary": summary_response.get("summary", "No summary received"),
    }


# ---------------------------------------------------------------------------
# Example usage (for local testing only)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import time

    now = int(time.time())
    filters = [{"resource_id": "i-0abcd1234"}]
    result = metric_summary("cpu.usage", filters=filters)
    print(json.dumps(result, indent=2))
