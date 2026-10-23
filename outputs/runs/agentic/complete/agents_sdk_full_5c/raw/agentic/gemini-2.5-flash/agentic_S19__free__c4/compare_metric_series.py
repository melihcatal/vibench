from google.cloud import monitoring_v3
from datetime import datetime, timedelta

def compare_metric_series(project_id: str, metric_type: str, filter1: str, filter2: str, minutes_ago: int = 60):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now
    start_time = now - timedelta(minutes=minutes_ago)

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(end_time.timestamp())},
        start_time={'seconds': int(start_time.timestamp())}
    )

    def _fetch_series(current_filter: str):
        query_filter = f'metric.type = "{metric_type}" AND {current_filter}'
        result = client.list_time_series(
            request={
                "name": project_name,
                "filter": query_filter,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            }
        )
        series_data = []
        for series in result:
            for point in series.points:
                series_data.append({
                    "metric": series.metric.type,
                    "resource_labels": dict(series.resource.labels),
                    "metric_labels": dict(series.metric.labels),
                    "value": point.value.double_value or point.value.int64_value,
                    "timestamp": point.interval.end_time.ToDatetime().isoformat(),
                })
        return series_data

    series_1 = _fetch_series(filter1)
    series_2 = _fetch_series(filter2)

    return {"series_1": series_1, "series_2": series_2}
