from datetime import datetime, timedelta, timezone
from observability_client import get_metrics_client, load_observability_config
from observability_models import MetricQuery, normalize_time_window, response_to_payload


def metric_summary(metric_name, start_time=None, end_time=None, dimensions=None):
    cfg = load_observability_config()
    client = get_metrics_client(cfg)
    end_time = end_time or datetime.now(timezone.utc)
    start_time = start_time or (end_time - timedelta(hours=12))
    start_time, end_time = normalize_time_window(start_time, end_time)
    query = MetricQuery(metric_name=metric_name, start_time=start_time, end_time=end_time, dimensions=dimensions or {}, period=300)
    kwargs = {'Namespace': cfg.namespace, 'MetricName': query.metric_name, 'StartTime': query.start_time, 'EndTime': query.end_time, 'Period': query.period, 'Statistics': ['Average', 'Maximum', 'Minimum', 'Sum']}
    if query.dimensions:
        kwargs['Dimensions'] = [{'Name': k, 'Value': v} for k, v in query.dimensions.items()]
    result = client.get_metric_statistics(**kwargs)
    payload = response_to_payload(result, query)
    values = [d.get('Average') for d in payload['datapoints'] if 'Average' in d]
    payload['trend'] = {'count': len(values), 'latest': values[-1] if values else None, 'peak': max(values) if values else None}
    return payload
