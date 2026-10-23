from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from observability_client import get_metric_data, load_observability_config
from observability_models import MetricWindowRequest, window_start


def aggregate_metric_stats(namespace: Optional[str] = None, metric_name: Optional[str] = None, minutes: int = 60, period: int = 300, dimensions: Optional[Dict[str, str]] = None, statistics: Optional[List[str]] = None, client: Optional[Any] = None):
    config = load_observability_config()
    request = MetricWindowRequest(
        namespace=namespace or config["namespace"],
        metric_name=metric_name or config["metric_name"],
        start_time=window_start(minutes),
        end_time=datetime.now(timezone.utc),
        period=period,
        statistics=statistics or ["Average", "Minimum", "Maximum", "SampleCount"],
        dimensions=dimensions or {},
    )
    return get_metric_data(request, client=client)
