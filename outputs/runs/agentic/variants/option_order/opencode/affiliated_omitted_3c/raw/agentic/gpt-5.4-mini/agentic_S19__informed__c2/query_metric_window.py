import os
from datetime import datetime, timedelta, timezone
from observability_client import get_metrics_client, load_observability_config
from observability_models import MetricQuery, normalize_time_window, response_to_payload


def query_metric_window(metric_name, start_time=None, end_time=None, dimensions=None, period=60):
    cfg = load_observability_config()
    client = get_metrics_client(cfg)
    end_time = end_time or datetime.now(timezone.utc)
    start_time = start_time or (end_time - timedelta(hours=1))
    start_time, end_time = normalize_time_window(start_time, end_time)
    query = MetricQuery(metric_name=metric_name, start_time=start_time, end_time=end_time, dimensions=dimensions or {}, period=period)
    kwargs = {
        'Namespace': cfg.namespace,
        'MetricName': query.metric_name,
        'StartTime': query.start_time,
        'EndTime': query.end_time,
        'Period': query.period,
        'Statistics': ['Average', 'Minimum', 'Maximum', 'Sum', 'SampleCount'],
    }
    if query.dimensions:
        kwargs['Dimensions'] = [{'Name': k, 'Value': v} for k, v in query.dimensions.items()]
    result = client.get_metric_statistics(**kwargs)
    return response_to_payload(result, query)
