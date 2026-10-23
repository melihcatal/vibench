from observability_client import DatadogMetricsClient


def compare_metric_series(metric, left_filters, right_filters, start_time=None, end_time=None):
    return DatadogMetricsClient().compare_metric_series(metric, left_filters, right_filters, start_time=start_time, end_time=end_time)
