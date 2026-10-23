import os
from observability_client import MonitoringClient

def filter_metric_dimensions(metric_name, filter_expr, start_time, end_time, **kwargs):
    """Query metric data filtered by resource labels or dimensions.

    Uses Google Cloud Monitoring (Stackdriver) Metrics API.
    Auth: GOOGLE_APPLICATION_CREDENTIALS.
    """
    client = MonitoringClient()
    window = {'start_time': start_time, 'end_time': end_time}
    query = client.build_query(metric=metric_name, window=window,
                               filter_expr=filter_expr)
    response = client.fetch_filtered_series(query)
    return response
