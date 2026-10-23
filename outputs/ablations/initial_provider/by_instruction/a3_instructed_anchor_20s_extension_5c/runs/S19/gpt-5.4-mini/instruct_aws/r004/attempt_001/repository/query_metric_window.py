from datetime import datetime, timezone
from typing import Any, Dict, Optional

from observability_client import get_metric_data, load_observability_config
from observability_models import MetricWindowRequest, parse_metric_data_results, window_start


def query_metric_window(namespace: Optional[str] = None, metric_name: Optional[str] = None, minutes: int = 60, period: int = 60, dimensions: Optional[Dict[str, str]] = None, statistics: Optional[list] = None, client: Optional[Any] = None):
    config = load_observability_config()
    request = MetricWindowRequest(
        namespace=namespace or config["namespace"],
        metric_name=metric_name or config["metric_name"],
        start_time=window_start(minutes),
        end_time=datetime.now(timezone.utc),
        period=period,
        statistics=statistics or ["Average"],
        dimensions=dimensions or {},
    )
    response = get_metric_data(request, client=client)
    return parse_metric_data_results(response.get("MetricDataResults", []))
