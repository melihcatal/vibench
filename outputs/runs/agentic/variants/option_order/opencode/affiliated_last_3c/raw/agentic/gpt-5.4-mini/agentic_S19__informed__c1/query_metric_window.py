from observability_client import DatadogMetricsClient


def query_metric_window(metric, start_time=None, end_time=None, filters=None, limit=1000):
    return DatadogMetricsClient().query_metric(metric, start_time=start_time, end_time=end_time, filters=filters, limit=limit)
