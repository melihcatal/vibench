from typing import Any, Dict

from query_metric_window import query_metric_window


def filter_metric_dimensions(
    metric_name: str, start_time: Any, end_time: Any, labels: Dict[str, Any]
) -> Dict[str, Any]:
    return query_metric_window(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        dimensions=labels,
    )
