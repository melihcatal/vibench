from observability_client import get_metric_data
from observability_models import MetricQuery


def compare_metric_series(
    metric_name,
    start_time,
    end_time,
    left_dimensions,
    right_dimensions,
    namespace=None,
    period=300,
    statistic="Average",
):
    left = get_metric_data(
        MetricQuery(
            metric_name=metric_name,
            start_time=start_time,
            end_time=end_time,
            namespace=namespace,
            period=period,
            statistic=statistic,
            dimensions=left_dimensions,
        )
    )
    right = get_metric_data(
        MetricQuery(
            metric_name=metric_name,
            start_time=start_time,
            end_time=end_time,
            namespace=namespace,
            period=period,
            statistic=statistic,
            dimensions=right_dimensions,
        )
    )
    return {"left": left, "right": right}
