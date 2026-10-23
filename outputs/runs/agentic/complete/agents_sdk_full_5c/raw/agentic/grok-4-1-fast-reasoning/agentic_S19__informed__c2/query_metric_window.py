from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import os
from typing import List
from observability_client import get_google_cloud_project
from observability_models import DataPoint

def query_metric_window(metric_name: str, window_hours: int = 1) -> List[DataPoint]:
    project_id = get_google_cloud_project()
    client = monitoring_v3.MetricServiceClient()
    end_time = Timestamp()
    end_time.GetCurrentTime()
    start_time = Timestamp()
    start_time.FromSeconds(int((datetime.utcnow() - timedelta(hours=window_hours)).timestamp()))
    interval = monitoring_v3.types.TimeInterval(start_time=start_time, end_time=end_time)
    filter_ = f'metric.type = "{metric_name}"'
    request = monitoring_v3.ListTimeSeriesRequest(
        name=f'projects/{project_id}',
        filter=filter_,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesView.FULL,
    )
    time_series_iter = client.list_time_series(request)
    datapoints = []
    for time_series in time_series_iter:
        for point in time_series.points:
            if point.value.HasField('double_value'):
                datapoints.append(DataPoint(
                    timestamp=point.interval.end_time.ToDatetime(),
                    value=point.value.double_value
                ))
    return datapoints
