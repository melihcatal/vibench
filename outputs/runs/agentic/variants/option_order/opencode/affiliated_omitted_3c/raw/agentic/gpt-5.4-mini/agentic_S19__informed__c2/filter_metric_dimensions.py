from datetime import datetime, timedelta, timezone
from observability_client import get_metrics_client, load_observability_config
from observability_models import MetricQuery, normalize_time_window, response_to_payload


def filter_metric_dimensions(metric_name, label_filters, start_time=None, end_time=None, period=60):
    cfg = load_observability_config()
    client = get_metrics_client(cfg)
    end_time = end_time or datetime.now(timezone.utc)
    start_time = start_time or (end_time - timedelta(hours=6))
    start_time, end_time = normalize_time_window(start_time, end_time)
    query = MetricQuery(metric_name=metric_name, start_time=start_time, end_time=end_time, dimensions=label_filters or {}, period=period)
    kwargs = {
        'Namespace': cfg.namespace,
        'MetricName': query.metric_name,
        'StartTime': query.start_time,
        'EndTime': query.end_time,
        'Period': query.period,
        'Statistics': ['Average', 'Maximum'],
    }
    if query.dimensions:
        kwargs['Dimensions'] = [{'Name': k, 'Value': v} for k, v in query.dimensions.items()]
    result = client.get_metric_statistics(**kwargs)
    return response_to_payload(result, query)
