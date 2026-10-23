from observability_client import get_metric_data
from observability_models import MetricQuery


def query_metric_window(
    metric_name,
    start_time,
    end_time,
    namespace=None,
    period=300,
    statistic="Average",
    dimensions=None,
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
