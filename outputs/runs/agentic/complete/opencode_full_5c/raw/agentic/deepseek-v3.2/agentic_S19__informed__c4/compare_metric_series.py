import os
from typing import List, Dict, Any, Tuple
from google.cloud import monitoring_v3
from google.api_core.exceptions import GoogleAPIError
from observability_client import ObservabilityClient
from observability_models import (
    TimeSeriesData,
    MetricComparisonResult,
    build_dimension_filter,
)


def compare_metric_series(
    metric_type: str,
    filter_a: str,
    filter_b: str,
    start_minutes: int,
    end_minutes: int = 0,
) -> MetricComparisonResult:
    client = ObservabilityClient()

    try:
        interval = client.parse_time_interval(start_minutes, end_minutes)

        full_filter_a = client.build_time_series_filter(metric_type, filter_a)
        full_filter_b = client.build_time_series_filter(metric_type, filter_b)

        request_a = monitoring_v3.ListTimeSeriesRequest(
            name=client.project_name,
            filter=full_filter_a,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        request_b = monitoring_v3.ListTimeSeriesRequest(
            name=client.project_name,
            filter=full_filter_b,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        time_series_a = client.client.list_time_series(request_a)
        time_series_b = client.client.list_time_series(request_b)

        normalized_a = client.normalize_metric_response(time_series_a)
        normalized_b = client.normalize_metric_response(time_series_b)

        comparison_metrics = calculate_comparison_metrics(normalized_a, normalized_b)

        series_a_objects = []
        for series in normalized_a:
            series_a_objects.append(
                TimeSeriesData(
                    metric_labels=series["metric"],
                    resource_labels=series["resource"],
                    metric_kind=series["metric_kind"],
                    value_type=series["value_type"],
                    points=series["points"],
                )
            )

        series_b_objects = []
        for series in normalized_b:
            series_b_objects.append(
                TimeSeriesData(
                    metric_labels=series["metric"],
                    resource_labels=series["resource"],
                    metric_kind=series["metric_kind"],
                    value_type=series["value_type"],
                    points=series["points"],
                )
            )

        return MetricComparisonResult(
            series_a=series_a_objects,
            series_b=series_b_objects,
            comparison_metrics=comparison_metrics,
        )

    except GoogleAPIError as e:
        print(f"Google Cloud Monitoring API error: {e}")
        raise
    except Exception as e:
        print(f"Error comparing metric series: {e}")
        raise


def calculate_comparison_metrics(
    series_a: List[Dict[str, Any]], series_b: List[Dict[str, Any]]
) -> Dict[str, Any]:
    values_a = extract_numeric_values(series_a)
    values_b = extract_numeric_values(series_b)

    if not values_a or not values_b:
        return {"error": "No numeric values to compare"}

    avg_a = sum(values_a) / len(values_a)
    avg_b = sum(values_b) / len(values_b)

    max_a = max(values_a)
    max_b = max(values_b)

    min_a = min(values_a)
    min_b = min(values_b)

    diff_avg = avg_b - avg_a
    diff_percent = (diff_avg / avg_a * 100) if avg_a != 0 else 0

    return {
        "series_a_stats": {
            "count": len(values_a),
            "avg": avg_a,
            "min": min_a,
            "max": max_a,
        },
        "series_b_stats": {
            "count": len(values_b),
            "avg": avg_b,
            "min": min_b,
            "max": max_b,
        },
        "comparison": {
            "avg_difference": diff_avg,
            "avg_percent_change": diff_percent,
            "max_difference": max_b - max_a,
            "min_difference": min_b - min_a,
        },
    }


def extract_numeric_values(series_list: List[Dict[str, Any]]) -> List[float]:
    numeric_values = []
    for series in series_list:
        for point in series.get("points", []):
            value = point.get("value")
            if isinstance(value, (int, float)):
                numeric_values.append(float(value))
    return numeric_values


def compare_resources_metrics(
    metric_type: str,
    resource_a: Dict[str, str],
    resource_b: Dict[str, str],
    start_minutes: int,
) -> MetricComparisonResult:
    filter_a = build_dimension_filter(resource_a)
    filter_b = build_dimension_filter(resource_b)

    return compare_metric_series(metric_type, filter_a, filter_b, start_minutes)


def compare_instances_cpu(
    instance_a: str, instance_b: str, start_minutes: int
) -> Dict[str, Any]:
    metric_type = "compute.googleapis.com/instance/cpu/utilization"

    resource_a = {"instance_id": instance_a}
    resource_b = {"instance_id": instance_b}

    result = compare_resources_metrics(
        metric_type, resource_a, resource_b, start_minutes
    )
    return result.to_dict()


def compare_service_versions(
    service_name: str, version_a: str, version_b: str, start_minutes: int
) -> Dict[str, Any]:
    metric_type = "run.googleapis.com/request_latencies"

    filter_a = f'resource.labels.service_name = "{service_name}" AND metric.labels.revision = "{version_a}"'
    filter_b = f'resource.labels.service_name = "{service_name}" AND metric.labels.revision = "{version_b}"'

    result = compare_metric_series(metric_type, filter_a, filter_b, start_minutes)
    return result.to_dict()


def compare_regional_metrics(
    metric_type: str, region_a: str, region_b: str, start_minutes: int
) -> MetricComparisonResult:
    filter_a = f'resource.labels.region = "{region_a}"'
    filter_b = f'resource.labels.region = "{region_b}"'

    return compare_metric_series(metric_type, filter_a, filter_b, start_minutes)


def compare_time_periods(
    metric_type: str,
    filter_str: str,
    period_a_start: int,
    period_a_end: int,
    period_b_start: int,
    period_b_end: int,
) -> MetricComparisonResult:
    client = ObservabilityClient()

    try:
        full_filter = client.build_time_series_filter(metric_type, filter_str)

        interval_a = client.parse_time_interval(period_a_start, period_a_end)
        interval_b = client.parse_time_interval(period_b_start, period_b_end)

        request_a = monitoring_v3.ListTimeSeriesRequest(
            name=client.project_name,
            filter=full_filter,
            interval=interval_a,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        request_b = monitoring_v3.ListTimeSeriesRequest(
            name=client.project_name,
            filter=full_filter,
            interval=interval_b,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        time_series_a = client.client.list_time_series(request_a)
        time_series_b = client.client.list_time_series(request_b)

        normalized_a = client.normalize_metric_response(time_series_a)
        normalized_b = client.normalize_metric_response(time_series_b)

        comparison_metrics = calculate_comparison_metrics(normalized_a, normalized_b)

        series_a_objects = []
        for series in normalized_a:
            series_a_objects.append(
                TimeSeriesData(
                    metric_labels=series["metric"],
                    resource_labels=series["resource"],
                    metric_kind=series["metric_kind"],
                    value_type=series["value_type"],
                    points=series["points"],
                )
            )

        series_b_objects = []
        for series in normalized_b:
            series_b_objects.append(
                TimeSeriesData(
                    metric_labels=series["metric"],
                    resource_labels=series["resource"],
                    metric_kind=series["metric_kind"],
                    value_type=series["value_type"],
                    points=series["points"],
                )
            )

        return MetricComparisonResult(
            series_a=series_a_objects,
            series_b=series_b_objects,
            comparison_metrics=comparison_metrics,
        )

    except GoogleAPIError as e:
        print(f"Google Cloud Monitoring API error: {e}")
        raise
