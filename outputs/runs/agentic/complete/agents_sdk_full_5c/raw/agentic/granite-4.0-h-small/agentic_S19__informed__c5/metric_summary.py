import os
from observability_client import MonitoringClient
from observability_models import MetricQueryRequest, MetricResponse


def metric_summary(metric_query: MetricQueryRequest):
    """Summarize recent metric trends or anomalies for a given query.

    Uses Google Cloud Monitoring (Stackdriver) Metrics API.
    Auth: GOOGLE_APPLICATION_CREDENTIALS.
    """
    client = MonitoringClient()
    query_dict = metric_query.to_dict()
    raw = client.fetch_time_series(query_dict)
    summary = {
        'metric': query_dict['metric'],
        'time_window': {
            'start': query_dict['interval']['start_time']['seconds'],
            'end': query_dict['interval']['end_time']['seconds']
        },
        'sample_count': len(raw),
        # Compute simple statistics on the most recent sample values
        'recent_values': [
            s['samples'][0]['value'] if s['samples'] else None
            for s in raw
        ]
    }
    return summary
