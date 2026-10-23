from datetime import datetime, timedelta, timezone
from observability_client import get_metrics_client, load_observability_config
from observability_models import MetricQuery, normalize_time_window, response_to_payload, compare_series_payload


def compare_metric_series(metric_name, left_dimensions, right_dimensions, start_time=None, end_time=None, period=60):
    cfg = load_observability_config()
    client = get_metrics_client(cfg)
    end_time = end_time or datetime.now(timezone.utc)
    start_time = start_time or (end_time - timedelta(hours=6))
    start_time, end_time = normalize_time_window(start_time, end_time)
    left_query = MetricQuery(metric_name=metric_name, start_time=start_time, end_time=end_time, dimensions=left_dimensions or {}, period=period)
    right_query = MetricQuery(metric_name=metric_name, start_time=start_time, end_time=end_time, dimensions=right_dimensions or {}, period=period)
    def fetch(query):
        kwargs = {
            'Namespace': cfg.namespace,
            'MetricName': query.metric_name,
            'StartTime': query.start_time,
            'EndTime': query.end_time,
            'Period': query.period,
            'Statistics': ['Average', 'Minimum', 'Maximum', 'Sum'],
        }
        if query.dimensions:
            kwargs['Dimensions'] = [{'Name': k, 'Value': v} for k, v in query.dimensions.items()]
        return response_to_payload(client.get_metric_statistics(**kwargs), query)
    return compare_series_payload(fetch(left_query), fetch(right_query))
