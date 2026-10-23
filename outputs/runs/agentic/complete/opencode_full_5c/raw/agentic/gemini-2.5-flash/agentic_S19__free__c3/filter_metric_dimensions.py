import os
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import ObservabilityClient
from observability_models import TimeSeriesData
from typing import Dict, List


def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    start_time: datetime,
    resource_labels: Dict[str, str],
) -> List[TimeSeriesData]:
    client = ObservabilityClient(project_id).get_monitoring_client()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time=Timestamp(seconds=int(end_time.timestamp())),
        start_time=Timestamp(seconds=int(start_time.timestamp())),
    )

    label_filters = []
    for key, value in resource_labels.items():
        label_filters.append(f'resource.labels.{key} = "{value}"')

    # Combine metric type filter with resource label filters
    filter_str = f'metric.type = "{metric_type}"'
    if label_filters:
        filter_str += " AND " + " AND ".join(label_filters)

    query_params = {
        "name": project_name,
        "filter": filter_str,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    response = client.list_time_series(**query_params)

    results = []
    for ts in response.time_series:
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
        results.append(
            TimeSeriesData(
                metric_type=ts.metric.type,
                resource_labels=dict(ts.resource.labels),
                points=points_data,
            )
        )
    return results
