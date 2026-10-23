import os
from observability_client import MonitoringClient

def aggregate_metric_stats(metric_name, start_time, end_time, aggregation='sum', **kwargs):
    """Retrieve aggregated statistics for a metric over a time window.

    Uses Google Cloud Monitoring (Stackdriver) Metrics API.
    Auth credentials: GOOGLE_APPLICATION_CREDENTIALS env var.
    """
    client = MonitoringClient()
    window = {'start_time': start_time, 'end_time': end_time}
    query = client.build_query(metric=metric_name, window=window,
                               aggregation={'alignment_period': None,
                                            'per_series_aligner': None,
                                            'cross_series_reducer': aggregation})
    response = client.fetch_aggregated_stats(query)
    return response
