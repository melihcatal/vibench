import os
from observability_client import MonitoringClient

def compare_metric_series(metric_name, filter_a, filter_b, start_time, end_time, **kwargs):
    """Compare metric values for two resources/label sets over the same window.

    Uses Google Cloud Monitoring (Stackdriver) Metrics API.
    Auth: GOOGLE_APPLICATION_CREDENTIALS.
    """
    client = MonitoringClient()
    window = {'start_time': start_time, 'end_time': end_time}
    query_a = client.build_query(metric=metric_name, window=window, filter_expr=filter_a)
    query_b = client.build_query(metric=metric_name, window=window, filter_expr=filter_b)
    res_a = client.fetch_time_series(query_a)
    res_b = client.fetch_time_series(query_b)
    # Simple side‑by‑side dict comparison
    return {'resource_a': res_a, 'resource_b': res_b}
