import os
from typing import List, Dict, Any, Optional
from google.cloud import monitoring_v3
from google.api_core.exceptions import GoogleAPIError
from observability_client import ObservabilityClient
from observability_models import (
    TimeSeriesData,
    MetricPoint,
    MetricKind,
    ValueType,
    build_dimension_filter,
)


def query_metrics_by_dimensions(
    metric_type: str,
    dimensions: Dict[str, str],
    start_minutes: int,
    end_minutes: int = 0,
) -> List[TimeSeriesData]:
    client = ObservabilityClient()

    try:
        filter_str = build_dimension_filter(dimensions)
        full_filter = client.build_time_series_filter(metric_type, filter_str)
        interval = client.parse_time_interval(start_minutes, end_minutes)

        request = monitoring_v3.ListTimeSeriesRequest(
            name=client.project_name,
            filter=full_filter,
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
        print(f"Error querying metrics by dimensions: {e}")
        raise


def filter_metrics_by_resource_labels(
    metric_type: str,
    resource_labels: Dict[str, str],
    start_minutes: int,
    end_minutes: int = 0,
) -> List[Dict[str, Any]]:
    data = query_metrics_by_dimensions(
        metric_type, resource_labels, start_minutes, end_minutes
    )
    return [ts.to_dict() for ts in data]


def query_metrics_by_metric_labels(
    metric_type: str,
    metric_labels: Dict[str, str],
    start_minutes: int,
    end_minutes: int = 0,
) -> List[TimeSeriesData]:
    client = ObservabilityClient()

    try:
        filters = []
        for key, value in metric_labels.items():
            filters.append(f'metric.labels.{key} = "{value}"')
        filter_str = " AND ".join(filters)

        full_filter = client.build_time_series_filter(metric_type, filter_str)
        interval = client.parse_time_interval(start_minutes, end_minutes)

        request = monitoring_v3.ListTimeSeriesRequest(
            name=client.project_name,
            filter=full_filter,
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


def get_metrics_by_instance_zone(
    instance_id: str, zone: str, start_minutes: int
) -> List[Dict[str, Any]]:
    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    dimensions = {"instance_id": instance_id, "zone": zone}
    return filter_metrics_by_resource_labels(metric_type, dimensions, start_minutes)


def get_metrics_by_service_version(
    service_name: str, version: str, start_minutes: int
) -> List[Dict[str, Any]]:
    metric_type = "run.googleapis.com/container/instance_count"
    dimensions = {"service_name": service_name, "revision_name": version}
    return filter_metrics_by_resource_labels(metric_type, dimensions, start_minutes)


def query_metrics_with_complex_filter(
    metric_type: str,
    resource_filters: Dict[str, str],
    metric_filters: Dict[str, str],
    start_minutes: int,
) -> List[TimeSeriesData]:
    client = ObservabilityClient()

    try:
        resource_parts = []
        for key, value in resource_filters.items():
            resource_parts.append(f'resource.labels.{key} = "{value}"')

        metric_parts = []
        for key, value in metric_filters.items():
            metric_parts.append(f'metric.labels.{key} = "{value}"')

        all_filters = resource_parts + metric_parts
        filter_str = " AND ".join(all_filters)

        full_filter = client.build_time_series_filter(metric_type, filter_str)
        interval = client.parse_time_interval(start_minutes)

        request = monitoring_v3.ListTimeSeriesRequest(
            name=client.project_name,
            filter=full_filter,
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
