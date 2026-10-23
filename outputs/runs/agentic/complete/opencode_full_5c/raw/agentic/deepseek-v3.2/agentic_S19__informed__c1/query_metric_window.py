import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import pytz


def query_metric_window(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    project_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Query recent datapoints for a named metric over a time window using Google Cloud Monitoring.

    Args:
        metric_name: The metric type name (e.g., 'compute.googleapis.com/instance/cpu/utilization')
        start_time: Start of the time window
        end_time: End of the time window
        project_id: Google Cloud project ID (defaults to GOOGLE_CLOUD_PROJECT env var)

    Returns:
        List of datapoints with timestamp and value
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable"
            )

    client = monitoring_v3.MetricServiceClient()

    project_name = f"projects/{project_id}"

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
        filter=f'metric.type = "{metric_name}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    results = []
    for time_series in client.list_time_series(request):
        for point in time_series.points:
            point_time = point.interval.end_time.ToDatetime()
            point_value = point.value.double_value or point.value.int64_value or 0

            results.append(
                {
                    "timestamp": point_time.isoformat(),
                    "value": point_value,
                    "metric_type": time_series.metric.type,
                    "resource_type": time_series.resource.type,
                    "labels": dict(time_series.metric.labels),
                }
            )

    return results


if __name__ == "__main__":
    end_time = datetime.now(pytz.UTC)
    start_time = end_time - timedelta(hours=1)

    datapoints = query_metric_window(
        metric_name="compute.googleapis.com/instance/cpu/utilization",
        start_time=start_time,
        end_time=end_time,
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    )

    print(f"Retrieved {len(datapoints)} datapoints")
