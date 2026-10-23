import os
from typing import List, Dict, Any
from google.cloud import monitoring_v3
from google.api_core.exceptions import GoogleAPIError
from observability_client import ObservabilityClient
from observability_models import TimeSeriesData, MetricPoint, MetricKind, ValueType


def query_recent_metric_data(
    metric_type: str, start_minutes: int, end_minutes: int = 0
) -> List[TimeSeriesData]:
    client = ObservabilityClient()

    try:
        filter_str = client.build_time_series_filter(metric_type)
        interval = client.parse_time_interval(start_minutes, end_minutes)

        request = monitoring_v3.ListTimeSeriesRequest(
            name=client.project_name,
            filter=filter_str,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        time_series = client.client.list_time_series(request)

        normalized_data = []
        for series in time_series:
            metric_kind = MetricKind[series.metric_kind.name]
            value_type = ValueType[series.value_type.name]

            points = []
            for point in series.points:
                metric_point = MetricPoint(
                    timestamp=point.interval.end_time,
                    value=client._extract_point_value(point, series.value_type),
                )
                points.append(metric_point)

            time_series_data = TimeSeriesData(
                metric_labels=dict(series.metric.labels),
                resource_labels=dict(series.resource.labels)
                if series.resource.labels
                else {},
                metric_kind=metric_kind,
                value_type=value_type,
                points=points,
            )
            normalized_data.append(time_series_data)

        return normalized_data

    except GoogleAPIError as e:
        print(f"Google Cloud Monitoring API error: {e}")
        raise
    except Exception as e:
        print(f"Error querying metric data: {e}")
        raise


def query_metric_with_custom_filter(
    metric_type: str, filter_str: str, start_minutes: int, end_minutes: int = 0
) -> List[TimeSeriesData]:
    client = ObservabilityClient()

    try:
        full_filter = client.build_time_series_filter(metric_type, filter_str)
        interval = client.parse_time_interval(start_minutes, end_minutes)

        request = monitoring_v3.ListTimeSeriesRequest(
            name=client.project_name,
            filter=full_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        time_series = client.client.list_time_series(request)

        return client.normalize_metric_response(time_series)

    except GoogleAPIError as e:
        print(f"Google Cloud Monitoring API error: {e}")
        raise


def get_metric_data_points(
    metric_type: str, start_minutes: int, end_minutes: int = 0
) -> List[Dict[str, Any]]:
    data = query_recent_metric_data(metric_type, start_minutes, end_minutes)
    return [ts.to_dict() for ts in data]


def query_cpu_utilization(instance_id: str, start_minutes: int) -> List[TimeSeriesData]:
    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    filter_str = f'resource.labels.instance_id = "{instance_id}"'
    return query_metric_with_custom_filter(metric_type, filter_str, start_minutes)


def query_http_requests(service_name: str, start_minutes: int) -> List[TimeSeriesData]:
    metric_type = "run.googleapis.com/request_count"
    filter_str = f'resource.labels.service_name = "{service_name}"'
    return query_metric_with_custom_filter(metric_type, filter_str, start_minutes)
