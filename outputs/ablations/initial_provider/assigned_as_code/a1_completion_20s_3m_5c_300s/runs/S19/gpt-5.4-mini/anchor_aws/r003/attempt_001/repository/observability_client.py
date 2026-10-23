import os
from typing import Any, Dict

import boto3

from observability_models import cloudwatch_dimensions, datapoints_to_series, normalize_dimensions


def load_observability_config(config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    merged = dict(config or {})
    merged.setdefault("region", os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    merged.setdefault("namespace", os.getenv("CLOUDWATCH_NAMESPACE", "Managed/Metrics"))
    merged.setdefault("period_seconds", int(os.getenv("CLOUDWATCH_PERIOD_SECONDS", "60")))
    merged.setdefault("statistic", os.getenv("CLOUDWATCH_STATISTIC", "Average"))
    merged["dimensions"] = normalize_dimensions(merged.get("dimensions", {}))
    return merged


def cloudwatch_client(config: Dict[str, Any] | None = None):
    cfg = load_observability_config(config)
    return boto3.client("cloudwatch", region_name=cfg.get("region"))


def metric_statistics(client, config: Dict[str, Any], metric: str, start_time, end_time, dimensions=None, statistics=None):
    cfg = load_observability_config(config)
    response = client.get_metric_statistics(
        Namespace=cfg["namespace"],
        MetricName=metric,
        Dimensions=cloudwatch_dimensions(dimensions or cfg.get("dimensions", {})),
        StartTime=start_time,
        EndTime=end_time,
        Period=cfg.get("period_seconds", 60),
        Statistics=statistics or [cfg.get("statistic", "Average")],
    )
    return datapoints_to_series(response.get("Datapoints", []))
