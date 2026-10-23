import os
from typing import Any, Dict, List, Optional

from google.cloud import monitoring_v3


def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    resource_filters: Optional[Dict[str, str]] = None,
    metric_filters: Optional[Dict[str, str]] = None,
    time_interval_seconds: int = 3600,
) -> List[Dict[str, Any]]:
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    interval = monitoring_v3.TimeInterval()
    interval.end_time.seconds = int(__import__("time").time())
    interval.start_time.seconds = interval.end_time.seconds - time_interval_seconds

    filter_parts = [f'metric.type = "{metric_type}"']
    for key, value in (resource_filters or {}).items():
        filter_parts.append(f'resource.label."{key}" = "{value}"')
    for key, value in (metric_filters or {}).items():
        filter_parts.append(f'metric.label."{key}" = "{value}"')

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=" AND ".join(filter_parts),
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    results: List[Dict[str, Any]] = []
    for series in client.list_time_series(request=request):
        points = []
        for point in series.points:
            points.append(
                {
                    "value": point.value.to_json(),
                    "timestamp": point.interval.end_time.ToJsonString(),
                }
            )
        results.append(
            {
                "metric_type": series.metric.type,
                "resource_type": series.resource.type,
                "metric_labels": dict(series.metric.labels),
                "resource_labels": dict(series.resource.labels),
                "points": points,
            }
        )
    return results


def main() -> None:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    metric_type = os.environ["METRIC_TYPE"]
    resource_filters: Dict[str, str] = {}
    metric_filters: Dict[str, str] = {}
    results = filter_metric_dimensions(project_id, metric_type, resource_filters, metric_filters)
    for item in results:
        print(item)


if __name__ == "__main__":
    main()
