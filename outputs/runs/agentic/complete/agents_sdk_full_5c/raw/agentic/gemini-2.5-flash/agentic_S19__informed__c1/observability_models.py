
from typing import Dict, Any, List
from google.cloud import monitoring_v3

def normalize_time_series_point(point: monitoring_v3.Point, time_series: monitoring_v3.TimeSeries) -> Dict[str, Any]:
    """
    Normalizes a single time series point from Google Cloud Monitoring into a simpler dictionary.
    """
    value = None
    if point.value.double_value is not None: 
        value = point.value.double_value
    elif point.value.int64_value is not None:
        value = point.value.int64_value
    elif point.value.bool_value is not None:
        value = point.value.bool_value
    elif point.value.string_value is not None:
        value = point.value.string_value

    return {
        "timestamp": point.interval.end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "value": value,
        "metric_labels": {k: v for k, v in time_series.metric.labels.items()},
        "resource_labels": {k: v for k, v in time_series.resource.labels.items()},
        "metric_kind": time_series.metric_kind.name,
        "value_type": time_series.value_type.name,
    }

def normalize_list_time_series_response(response: monitoring_v3.ListTimeSeriesResponse) -> List[Dict[str, Any]]:
    """
    Normalizes a ListTimeSeriesResponse into a list of simplified dictionaries.
    """
    normalized_data = []
    for ts in response.time_series:
        for point in ts.points:
            normalized_data.append(normalize_time_series_point(point, ts))
    return normalized_data
