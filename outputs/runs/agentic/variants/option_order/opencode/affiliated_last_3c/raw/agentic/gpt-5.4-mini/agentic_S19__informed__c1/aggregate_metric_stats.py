from observability_client import DatadogMetricsClient


def aggregate_metric_stats(metric, start_time=None, end_time=None, filters=None, aggregation='avg'):
    return DatadogMetricsClient().get_aggregate_stats(metric, start_time=start_time, end_time=end_time, filters=filters, aggregation=aggregation)
