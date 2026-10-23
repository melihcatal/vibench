from typing import Dict, List, Optional, Union
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp


def normalize_timestamp(dt: Union[datetime, str, int]) -> Timestamp:
    """Convert various timestamp formats to Google Timestamp."""
    if isinstance(dt, Timestamp):
        return dt
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    if isinstance(dt, int):
        dt = datetime.fromtimestamp(dt)
    timestamp = Timestamp()
    timestamp.FromDatetime(dt)
    return timestamp


def parse_time_series_response(response):
    """Parse Google Cloud Monitoring time series response into a structured format."""
    series_list = []
    for series in response:
        points = []
        for point in series.points:
            points.append(
                {
                    "interval": {
                        "start_time": point.interval.start_time.ToDatetime(),
                        "end_time": point.interval.end_time.ToDatetime(),
                    },
                    "value": point.value.double_value
                    if point.value.double_value is not None
                    else point.value.int64_value,
                }
            )

        metric_labels = dict(series.metric.labels)
        resource_labels = dict(series.resource.labels)

        series_list.append(
            {
                "metric": {
                    "type": series.metric.type,
                    "labels": metric_labels,
                },
                "resource": {
                    "type": series.resource.type,
                    "labels": resource_labels,
                },
                "points": points,
            }
        )
    return series_list


def build_filter_from_dimensions(dimensions: Dict[str, str]) -> str:
    """Build a Google Cloud Monitoring filter string from dimension key-value pairs."""
    filters = []
    for key, value in dimensions.items():
        if key.startswith("resource."):
            filters.append(f'resource.label.{key[9:]}="{value}"')
        else:
            filters.append(f'metric.label.{key}="{value}"')
    return " AND ".join(filters)
