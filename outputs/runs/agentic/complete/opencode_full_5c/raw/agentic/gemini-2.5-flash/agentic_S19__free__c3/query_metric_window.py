import os
from datetime import datetime, timedelta
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import ObservabilityClient
from observability_models import TimeSeriesData


def query_metric_window(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    start_time: datetime,
) -> TimeSeriesData:
    client = ObservabilityClient(project_id).get_monitoring_client()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time=Timestamp(seconds=int(end_time.timestamp())),
        start_time=Timestamp(seconds=int(start_time.timestamp())),
    )

    query_params = {
        "name": project_name,
        "filter": f'metric.type = "{metric_type}"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    response = client.list_time_series(**query_params)

    # Assuming a single time series for simplicity; adjust if multiple are expected.
    # For a more robust solution, you might iterate through response.time_series.
    if response.time_series:
        ts = response.time_series[0]
        points_data = []
        for point in ts.points:
            points_data.append(
                {
                    "interval": {
                        "start_time": point.interval.start_time.isoformat(),
                        "end_time": point.interval.end_time.isoformat(),
                    },
                    "value": getattr(point.value, point.value.WhichOneof("value_type")),
                }
            )
        return TimeSeriesData(
            metric_type=ts.metric.type,
            resource_labels=dict(ts.resource.labels),
            points=points_data,
        )
    return TimeSeriesData(metric_type=metric_type, resource_labels={}, points=[])
