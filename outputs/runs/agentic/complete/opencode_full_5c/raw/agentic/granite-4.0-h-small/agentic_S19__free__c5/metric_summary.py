# [LATER-STEP] metric_summary.py

# Summarize recent metric trends or anomalies using New Relic as the provider.

from __future__ import annotations
from datetime import datetime, timedelta
import json

from observability_client import NewRelicClient
from observability_models import (
    MetricQueryRequest,
    MetricQueryResponse,
    MetricStatsRequest,
    MetricStatsResponse,
)


def summarize_recent_trends(
    metric_name: str, lookback: timedelta = timedelta(hours=24)
) -> dict:
    """
    Produce a concise summary of recent metric behavior:
    - Latest raw datapoint value.
    - Mean, min, max, count over the lookback window.
    - Simple anomaly flag (value > 2× avg).

    Returns a dict suitable for downstream dashboards or alerts.
    """
    now = datetime.utcnow()
    start = now - lookback
    # 1. Pull the latest single point (limit=1)
    latest_query = MetricQueryRequest(
        metric=metric_name,
        start=now,
        end=now + timedelta(seconds=1),  # effectively "now"
        limit=1,
    )
    latest_resp: MetricQueryResponse = NewRelicClient().query_metrics(
        latest_query.__dict__
    )
    latest_value = (
        latest_resp.datapoints[0]["value"] if latest_resp.datapoints else None
    )

    # 2. Pull aggregated stats over the lookback period
    stats_req = MetricStatsRequest(
        metric=metric_name,
        start=start,
        end=now,
    )
    stats_resp: MetricStatsResponse = NewRelicClient().get_stats(stats_req.__dict__)
    summary = {
        "metric": metric_name,
        "latest_value": latest_value,
        "stats": {
            "min": stats_resp.min,
            "max": stats_resp.max,
            "avg": stats_resp.avg,
            "count": stats_resp.count,
        },
    }
    # 3. Simple anomaly detection
    if stats_resp.avg and latest_value and stats_resp.avg != 0:
        summary["anomaly"] = latest_value > 2 * stats_resp.avg
    else:
        summary["anomaly"] = None
    return summary


if __name__ == "__main__":
    # Example: summarize CPU usage over the past 6 hours
    trend = summarize_recent_trends("cpu.usage.percent", lookback=timedelta(hours=6))
    print(json.dumps(trend, indent=2))
