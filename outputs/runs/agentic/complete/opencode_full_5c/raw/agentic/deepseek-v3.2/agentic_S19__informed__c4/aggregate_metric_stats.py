import os
from typing import List, Dict, Any, Optional
from google.cloud import monitoring_v3
from google.api_core.exceptions import GoogleAPIError
from observability_client import ObservabilityClient
from observability_models import MetricAggregationResult, parse_aggregation_response


def get_aggregated_metric_stats(
    metric_type: str,
    start_minutes: int,
    end_minutes: int = 0,
    aggregation: str = "REDUCE_SUM",
    alignment_period: str = "60s",
) -> MetricAggregationResult:
    client = ObservabilityClient()

    try:
        filter_str = client.build_time_series_filter(metric_type)
        interval = client.parse_time_interval(start_minutes, end_minutes)

        aggregation_obj = monitoring_v3.Aggregation()

        if aggregation == "REDUCE_SUM":
            aggregation_obj.per_series_aligner = (
                monitoring_v3.Aggregation.Aligner.ALIGN_SUM
            )
            aggregation_obj.cross_series_reducer = (
                monitoring_v3.Aggregation.Reducer.REDUCE_SUM
            )
        elif aggregation == "REDUCE_MEAN":
            aggregation_obj.per_series_aligner = (
                monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
            )
            aggregation_obj.cross_series_reducer = (
                monitoring_v3.Aggregation.Reducer.REDUCE_MEAN
            )
        elif aggregation == "REDUCE_MAX":
            aggregation_obj.per_series_aligner = (
                monitoring_v3.Aggregation.Aligner.ALIGN_MAX
            )
            aggregation_obj.cross_series_reducer = (
                monitoring_v3.Aggregation.Reducer.REDUCE_MAX
            )
        elif aggregation == "REDUCE_MIN":
            aggregation_obj.per_series_aligner = (
                monitoring_v3.Aggregation.Aligner.ALIGN_MIN
            )
            aggregation_obj.cross_series_reducer = (
                monitoring_v3.Aggregation.Reducer.REDUCE_MIN
            )
        else:
            aggregation_obj.per_series_aligner = (
                monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
            )
            aggregation_obj.cross_series_reducer = (
                monitoring_v3.Aggregation.Reducer.REDUCE_MEAN
            )

        aggregation_obj.alignment_period = {"seconds": 60}

        request = monitoring_v3.ListTimeSeriesRequest(
            name=client.project_name,
            filter=filter_str,
            interval=interval,
            aggregation=aggregation_obj,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        time_series = client.client.list_time_series(request)
        normalized_data = client.normalize_metric_response(time_series)

        return parse_aggregation_response(normalized_data)

    except GoogleAPIError as e:
        print(f"Google Cloud Monitoring API error: {e}")
        raise
    except Exception as e:
        print(f"Error aggregating metric stats: {e}")
        raise


def get_percentile_metrics(
    metric_type: str, start_minutes: int, percentiles: List[float] = [50, 95, 99]
) -> Dict[str, float]:
    client = ObservabilityClient()

    try:
        filter_str = client.build_time_series_filter(metric_type)
        interval = client.parse_time_interval(start_minutes)

        request = monitoring_v3.ListTimeSeriesRequest(
            name=client.project_name,
            filter=filter_str,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        time_series = client.client.list_time_series(request)
        normalized_data = client.normalize_metric_response(time_series)

        all_values = []
        for series in normalized_data:
            for point in series.get("points", []):
                value = point.get("value")
                if isinstance(value, (int, float)):
                    all_values.append(value)

        if not all_values:
            return {}

        all_values.sort()
        result = {}

        for percentile in percentiles:
            if percentile < 0 or percentile > 100:
                continue

            index = (percentile / 100) * (len(all_values) - 1)
            lower_index = int(index)
            upper_index = min(lower_index + 1, len(all_values) - 1)

            if lower_index == upper_index:
                result[f"p{int(percentile)}"] = all_values[lower_index]
            else:
                weight = index - lower_index
                value = (
                    all_values[lower_index] * (1 - weight)
                    + all_values[upper_index] * weight
                )
                result[f"p{int(percentile)}"] = value

        return result

    except GoogleAPIError as e:
        print(f"Google Cloud Monitoring API error: {e}")
        raise


def get_metric_statistics(
    metric_type: str, start_minutes: int, end_minutes: int = 0
) -> Dict[str, Any]:
    stats = get_aggregated_metric_stats(metric_type, start_minutes, end_minutes)
    percentiles = get_percentile_metrics(metric_type, start_minutes)

    result = stats.to_dict()
    if percentiles:
        result["percentiles"] = percentiles

    return result


def get_latency_statistics(service_name: str, start_minutes: int) -> Dict[str, Any]:
    metric_type = "run.googleapis.com/request_latencies"
    filter_str = f'resource.labels.service_name = "{service_name}"'

    client = ObservabilityClient()
    full_filter = client.build_time_series_filter(metric_type, filter_str)

    stats = get_aggregated_metric_stats(metric_type, start_minutes, 0, "REDUCE_MEAN")
    percentiles = get_percentile_metrics(metric_type, start_minutes)

    result = stats.to_dict()
    if percentiles:
        result["percentiles"] = percentiles

    return result


def get_error_rate_statistics(service_name: str, start_minutes: int) -> Dict[str, Any]:
    metric_type = "run.googleapis.com/container/instance_count"
    filter_str = f'resource.labels.service_name = "{service_name}" AND metric.labels.state = "error"'

    client = ObservabilityClient()
    full_filter = client.build_time_series_filter(metric_type, filter_str)

    return get_aggregated_metric_stats(
        metric_type, start_minutes, 0, "REDUCE_SUM"
    ).to_dict()
