from datetime import datetime, timedelta, timezone
from typing import Optional

from observability_client import cloudwatch_client, load_config
from observability_models import normalize_dimensions


def aggregate_metric_stats(metric_name: Optional[str] = None, namespace: Optional[str] = None, dimensions: Optional[dict] = None, minutes: int = 60):
    cfg = load_config(namespace=namespace, metric_name=metric_name)
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    client = cloudwatch_client()
    return client.get_metric_statistics(
        Namespace=cfg.namespace,
        MetricName=cfg.metric_name,
        Dimensions=normalize_dimensions(dimensions),
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average", "Sum", "Minimum", "Maximum", "SampleCount"],
    )
