from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import load_config, metric_scope_name
from observability_models import MetricWindowRequest


def query_metric_window(metric_type: str, minutes: int = 60):
    config = load_config()
    client = monitoring_v3.MetricServiceClient()
    project_name = metric_scope_name(config.gcp_project_id)
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    request = MetricWindowRequest(
        metric_type=metric_type,
        start_time=start_time.isoformat(),
        end_time=end_time.isoformat(),
        filter_expression=f'metric.type = "{metric_type}"',
    )
    interval = monitoring_v3.TimeInterval(
        {
            "start_time": request.start_time,
            "end_time": request.end_time,
        }
    )
    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": request.filter_expression,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    return [series for series in results]
