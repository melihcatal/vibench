from datetime import datetime, timedelta, timezone
from typing import Mapping, Optional

from observability_client import cloudwatch_client, load_config
from observability_models import normalize_dimensions


def compare_metric_series(
    first_dimensions: Optional[Mapping[str, str]] = None,
    second_dimensions: Optional[Mapping[str, str]] = None,
    metric_name: Optional[str] = None,
    namespace: Optional[str] = None,
    minutes: int = 60,
):
    cfg = load_config(namespace=namespace, metric_name=metric_name)
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    client = cloudwatch_client()
    first = client.get_metric_statistics(Namespace=cfg.namespace, MetricName=cfg.metric_name, Dimensions=normalize_dimensions(first_dimensions), StartTime=start_time, EndTime=end_time, Period=300, Statistics=["Average"])
    second = client.get_metric_statistics(Namespace=cfg.namespace, MetricName=cfg.metric_name, Dimensions=normalize_dimensions(second_dimensions), StartTime=start_time, EndTime=end_time, Period=300, Statistics=["Average"])
    return {"first": first, "second": second}
