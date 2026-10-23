import os
from observability_client import MonitoringClient

def query_metric_window(metric_name, start_time, end_time, **kwargs):
    """Query recent datapoints for a named metric over a time window.

    Uses Google Cloud Monitoring (Stackdriver) Metrics API.
    Auth credentials taken from env var GOOGLE_APPLICATION_CREDENTIALS.
    """
    client = MonitoringClient()
    window = {'start_time': start_time, 'end_time': end_time}
    query = client.build_query(metric=metric_name, window=window, **kwargs)
    response = client.fetch_time_series(query)
    return response
