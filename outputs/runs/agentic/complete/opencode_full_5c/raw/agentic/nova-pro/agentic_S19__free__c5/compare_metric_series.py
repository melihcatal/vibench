import boto3
from observability_client import cw_client
from observability_models import MetricData


def compare_metric_series(
    metric_name: str,
    start_time: str,
    end_time: str,
    period: int,
    dimensions1: Dict[str, str],
    dimensions2: Dict[str, str],
):
    data1 = filter_metric_dimensions(
        metric_name, start_time, end_time, period, dimensions1
    )
    data2 = filter_metric_dimensions(
        metric_name, start_time, end_time, period, dimensions2
    )
    return data1, data2
