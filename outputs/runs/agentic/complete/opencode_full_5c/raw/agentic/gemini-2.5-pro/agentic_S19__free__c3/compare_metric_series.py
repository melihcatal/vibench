from typing import Dict, List
from observability_models import MetricData
from filter_metric_dimensions import filter_metric_by_dimensions


def compare_metric_series(
    metric_name: str,
    dimensions1: Dict[str, str],
    dimensions2: Dict[str, str],
    minutes: int = 60,
) -> List[MetricData]:
    """
    Compares two metric series for the same metric but with different dimensions.
    """
    series1 = filter_metric_by_dimensions(metric_name, dimensions1, minutes)
    series2 = filter_metric_by_dimensions(metric_name, dimensions2, minutes)

    return series1 + series2
