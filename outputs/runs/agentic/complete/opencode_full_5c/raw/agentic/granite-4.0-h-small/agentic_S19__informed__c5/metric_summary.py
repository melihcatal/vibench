# metric_summary.py
# LATER-STEP implementation using Datadog Metrics API (Python requests)

import os
from datetime import datetime, timedelta
from typing import Any, Dict
from observability_client import ObservabilityClient
from observability_models import SummaryRequest, SummaryResponse

# Provider identifier for this file (visible in code)
PROVIDER = "datadog"


def summarize_metric(req: SummaryRequest) -> SummaryResponse:
    client = ObservabilityClient()
    # Compute the start of the requested window (e.g., "1h", "24h")
    now = datetime.utcnow()
    if req.window.endswith("h"):
        hours = int(req.window[:-1])
        start = now - timedelta(hours=hours)
    elif req.window.endswith("d"):
        days = int(req.window[:-1])
        start = now - timedelta(days=days)
    else:
        raise ValueError(f"Unsupported window format: {req.window}")
    end = now
    # Query recent datapoints
    payload = {
        "metric": req.metric,
        "start": start.isoformat() + "Z",
        "end": end.isoformat() + "Z",
        "tags": [],
    }
    raw = client.query_recent(**payload)
    normalized = client._normalize_response(PROVIDER, raw)
    datapoints = normalized.get("datapoints", [])
    if not datapoints:
        return SummaryResponse(
            metric=normalized["metric"], recent_value=None, trend="none"
        )
    # Simple trend using first vs last point
    first_val = float(datapoints[0][1])
    last_val = float(datapoints[-1][1])
    recent_value = last_val
    if first_val == 0:
        trend = "none" if last_val == 0 else "positive"
    else:
        trend = "positive" if last_val > first_val else "negative"
    return SummaryResponse(
        metric=normalized["metric"], recent_value=recent_value, trend=trend
    )


if __name__ == "__main__":
    # Example usage (remove or adapt when integrating into a real service)
    req = SummaryRequest(metric="system.cpu.idle", window="1h")
    result = summarize_metric(req)
    print(result)
