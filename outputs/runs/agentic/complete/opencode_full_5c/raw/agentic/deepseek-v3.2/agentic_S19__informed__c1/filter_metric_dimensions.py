import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import pytz


def filter_metric_dimensions(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    dimension_filters: Dict[str, str],
    project_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Query metric data filtered by resource labels or dimensions using Google Cloud Monitoring.

    Args:
        metric_name: The metric type name (e.g., 'compute.googleapis.com/instance/cpu/utilization')
        start_time: Start of the time window
        end_time: End of the time window
        dimension_filters: Dictionary of dimension name to value filters
        project_id: Google Cloud project ID (defaults to GOOGLE_CLOUD_PROJECT env var)

    Returns:
        List of filtered time series data
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable"
            )

    client = monitoring_v3.MetricServiceClient()

    project_name = f"projects/{project_id}"

    filter_parts = [f'metric.type = "{metric_name}"']
    for dim_name, dim_value in dimension_filters.items():
        filter_parts.append(f'resource.labels.{dim_name} = "{dim_value}"')

    filter_str = " AND ".join(filter_parts)

    interval = monitoring_v3.TimeInterval()
    interval.start_time = Timestamp()
    interval.start_time.FromDatetime(start_time)
    interval.end_time = Timestamp()
    interval.end_time.FromDatetime(end_time)

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period = {"seconds": 60}
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    results = []
    for time_series in client.list_time_series(request):
        series_data = {
            "metric_type": time_series.metric.type,
            "resource_type": time_series.resource.type,
            "resource_labels": dict(time_series.resource.labels),
            "metric_labels": dict(time_series.metric.labels),
            "points": [],
        }

        for point in time_series.points:
            point_time = point.interval.end_time.ToDatetime()
            point_value = point.value.double_value or point.value.int64_value or 0

            series_data["points"].append(
                {"timestamp": point_time.isoformat(), "value": point_value}
            )

        results.append(series_data)

    return results


if __name__ == "__main__":
    end_time = datetime.now(pytz.UTC)
    start_time = end_time - timedelta(hours=1)

    filtered_data = filter_metric_dimensions(
        metric_name="compute.googleapis.com/instance/cpu/utilization",
        start_time=start_time,
        end_time=end_time,
        dimension_filters={"instance_id": "my-instance-1", "zone": "us-central1-a"},
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    )

    print(f"Filtered {len(filtered_data)} time series")
    for series in filtered_data:
        print(
            f"  Resource: {series['resource_labels']}, Points: {len(series['points'])}"
        )
