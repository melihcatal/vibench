from datetime import datetime, timezone
from typing import Any, Dict, Optional

from observability_client import get_metric_data, load_observability_config
from observability_models import MetricWindowRequest, window_start


def metric_summary(namespace: Optional[str] = None, metric_name: Optional[str] = None, minutes: int = 240, period: int = 300, dimensions: Optional[Dict[str, str]] = None, client: Optional[Any] = None):
    config = load_observability_config()
    request = MetricWindowRequest(
        namespace=namespace or config["namespace"],
        metric_name=metric_name or config["metric_name"],
        start_time=window_start(minutes),
        end_time=datetime.now(timezone.utc),
        period=period,
        statistics=["Average", "Minimum", "Maximum"],
        dimensions=dimensions or {},
    )
    return get_metric_data(request, client=client)
