from google.cloud import monitoring_v3
from observability_client import get_client_config
from datetime import datetime, timedelta


def compare_metric_series(metric_type: str, filter_a: dict, filter_b: dict, hours: int = 1, project_id: str = None):
    config = get_client_config()
    project_id = project_id or config.get("GOOGLE_CLOUD_PROJECT")
    
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(end_time.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    def build_filter(base_filter: dict) -> str:
        filter_parts = [f"metric.type=\"{metric_type}\""]
        for key, value in base_filter.items():
            filter_parts.append(f"metric.labels.{key}=\"{value}\"")
        return " AND ".join(filter_parts)

    query_a = build_filter(filter_a)
    query_b = build_filter(filter_b)

    def fetch_series(query: str):
        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": query,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            }
        )
        return [
            {
                "metric": {
                    "type": series.metric.type,
                    "labels": dict(series.metric.labels),
                },
                "resource": {
                    "type": series.resource.type,
                    "labels": dict(series.resource.labels),
                },
                "points": [
                    {
                        "interval": {
                            "start_time": point.interval.start_time.ToDatetime(),
                            "end_time": point.interval.end_time.ToDatetime(),
                        },
                        "value": point.value.double_value,
                    }
                    for point in series.points
                ],
            }
            for series in results
        ]

    series_a = fetch_series(query_a)
    series_b = fetch_series(query_b)

    return {
        "series_a": series_a,
        "series_b": series_b,
        "comparison_window": {
            "start_time": start_time,
            "end_time": end_time,
        },
    }