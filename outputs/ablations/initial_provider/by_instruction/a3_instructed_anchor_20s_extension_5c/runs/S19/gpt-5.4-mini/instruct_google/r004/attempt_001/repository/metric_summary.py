from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import load_config, metric_scope_name


def metric_summary(metric_type: str, minutes: int = 120):
    config = load_config()
    client = monitoring_v3.MetricServiceClient()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    interval = monitoring_v3.TimeInterval({"start_time": start_time.isoformat(), "end_time": end_time.isoformat()})
    response = client.list_time_series(request={"name": metric_scope_name(config.gcp_project_id), "filter": f'metric.type = "{metric_type}"', "interval": interval, "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    return {"series_count": sum(1 for _ in response)}
