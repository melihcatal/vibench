from observability_client import DatadogMetricsClient


def filter_metric_dimensions(metric, dimensions, start_time=None, end_time=None):
    return DatadogMetricsClient().filter_metric_dimensions(metric, dimensions, start_time=start_time, end_time=end_time)
