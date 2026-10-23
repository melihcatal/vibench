from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import get_cloudwatch_client, load_config
from observability_models import MetricSummaryResponse


def metric_summary(metric_name: str, minutes: int = 120) -> MetricSummaryResponse:
    cfg = load_config()
    client = get_cloudwatch_client(cfg.region_name)
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    raw = client.get_metric_statistics(
        Namespace=cfg.namespace,
        MetricName=metric_name,
        StartTime=start,
        EndTime=end,
        Period=300,
        Statistics=["Average", "Maximum", "Minimum"],
    )
    dps = raw.get("Datapoints", [])
    values = sorted(float(dp.get("Average", dp.get("Maximum", dp.get("Minimum", 0.0)))) for dp in dps)
    if not values:
        return MetricSummaryResponse(metric_name=metric_name, summary="No recent datapoints", trend="flat", anomaly_score=0.0)
    trend = "rising" if values[-1] > values[0] else "falling" if values[-1] < values[0] else "flat"
    anomaly_score = float((max(values) - min(values)) / max(max(values), 1.0))
    return MetricSummaryResponse(metric_name=metric_name, summary=f"Observed {len(values)} datapoints", trend=trend, anomaly_score=anomaly_score)
