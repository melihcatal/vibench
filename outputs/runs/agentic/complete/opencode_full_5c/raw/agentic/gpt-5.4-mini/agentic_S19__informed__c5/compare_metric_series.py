from typing import Any, Dict

from query_metric_window import query_metric_window


def compare_metric_series(
    metric_name: str,
    start_time: Any,
    end_time: Any,
    left_dimensions: Dict[str, Any],
    right_dimensions: Dict[str, Any],
) -> Dict[str, Any]:
    left = query_metric_window(metric_name, start_time, end_time, left_dimensions)
    right = query_metric_window(metric_name, start_time, end_time, right_dimensions)
    return {"left": left, "right": right}
