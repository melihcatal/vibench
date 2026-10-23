from datetime import datetime, timedelta
from typing import List
import os

from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import get_monitoring_client
from observability_models import MetricQueryRequest, MetricPoint, MetricSeries


def query_metric_window(request: MetricQueryRequest) -> List[MetricSeries]:
    client = get_monitoring_client()

    # Convert datetime objects to Google Cloud Monitoring Timestamp format
    end_timestamp = Timestamp()
    end_timestamp.FromDatetime(request.end_time)
    start_timestamp = Timestamp()
    start_timestamp.FromDatetime(request.start_time)

    interval = monitoring_v3.TimeInterval(
        end_time=end_timestamp,
        start_time=start_timestamp,
    )

    query_filter = f'metric.type = "{request.metric_type}"'
    if request.filter_str:
        query_filter += f" AND {request.filter_str}"

    results = client.list_time_series(
        name=f"projects/{request.project_id}",
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    metric_series_list: List[MetricSeries] = []
    for time_series in results:
        points: List[MetricPoint] = []
        for point in time_series.points:
            point_time = point.interval.end_time.ToDatetime()
            # Assuming value_type is double_value for simplicity. Adjust if other types are needed.
            value = (
                point.value.double_value
                if point.value.HasField("double_value")
                else None
            )
            if value is not None:
                points.append(MetricPoint(time=point_time, value=value))

        labels = {k: v for k, v in time_series.metric.labels.items()}
        labels.update({k: v for k, v in time_series.resource.labels.items()})

        metric_series_list.append(MetricSeries(points=points, labels=labels))

    return metric_series_list
