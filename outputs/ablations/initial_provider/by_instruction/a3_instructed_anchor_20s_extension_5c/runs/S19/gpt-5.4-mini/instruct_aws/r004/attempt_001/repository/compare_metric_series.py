from datetime import datetime, timezone
from typing import Any, Dict, Optional

from observability_client import get_metric_data, load_observability_config
from observability_models import MetricWindowRequest, window_start


def compare_metric_series(namespace: Optional[str] = None, metric_name: Optional[str] = None, left_dimensions: Optional[Dict[str, str]] = None, right_dimensions: Optional[Dict[str, str]] = None, minutes: int = 60, period: int = 60, client: Optional[Any] = None):
    config = load_observability_config()
    base_namespace = namespace or config["namespace"]
    base_metric = metric_name or config["metric_name"]
    window_end = datetime.now(timezone.utc)
    left = MetricWindowRequest(base_namespace, base_metric, window_start(minutes), window_end, period=period, dimensions=left_dimensions or {})
    right = MetricWindowRequest(base_namespace, base_metric, window_start(minutes), window_end, period=period, dimensions=right_dimensions or {})
    return {
        "left": get_metric_data(left, client=client),
        "right": get_metric_data(right, client=client),
    }
