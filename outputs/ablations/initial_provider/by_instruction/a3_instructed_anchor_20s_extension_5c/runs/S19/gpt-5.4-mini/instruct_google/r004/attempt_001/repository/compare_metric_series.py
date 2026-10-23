from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import load_config, metric_scope_name


def compare_metric_series(metric_type: str, filter_a: str, filter_b: str, minutes: int = 60):
    config = load_config()
    client = monitoring_v3.MetricServiceClient()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    interval = monitoring_v3.TimeInterval(
        {"start_time": start_time.isoformat(), "end_time": end_time.isoformat()}
    )
    base = {"name": metric_scope_name(config.gcp_project_id), "interval": interval, "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL}
    response_a = client.list_time_series(request={**base, "filter": f'metric.type = "{metric_type}" AND {filter_a}'})
    response_b = client.list_time_series(request={**base, "filter": f'metric.type = "{metric_type}" AND {filter_b}'})
    return {"a": [s for s in response_a], "b": [s for s in response_b]}
