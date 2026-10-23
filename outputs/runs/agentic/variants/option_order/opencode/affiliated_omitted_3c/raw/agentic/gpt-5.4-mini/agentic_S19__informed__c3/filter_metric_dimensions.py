from observability_client import get_metric_data
from observability_models import MetricQuery


def filter_metric_dimensions(
    metric_name,
    start_time,
    end_time,
    dimensions,
    namespace=None,
    period=300,
    statistic="Average",
):
    query = MetricQuery(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        namespace=namespace,
        period=period,
        statistic=statistic,
        dimensions=dimensions,
    )
    return get_metric_data(query)
