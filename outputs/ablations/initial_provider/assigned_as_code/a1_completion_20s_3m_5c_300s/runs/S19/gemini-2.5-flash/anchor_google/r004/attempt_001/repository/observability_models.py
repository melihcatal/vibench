from typing import Dict, Any, List, Optional, Union

def normalize_time_series_response(time_series_list: List[Any]) -> List[Dict[str, Union[float, str]]]:
    """Normalizes Google Cloud Monitoring TimeSeries response into a simpler format."""
    normalized_points = []
    for time_series in time_series_list:
        metric_type = time_series.metric.type
        resource_labels = {k: v for k, v in time_series.resource.labels.items()}
        metric_labels = {k: v for k, v in time_series.metric.labels.items()}

        for point in time_series.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                continue  # Skip non-numeric values
            
            value = float(getattr(point.value, kind))
            timestamp = point.interval.end_time.timestamp()

            normalized_points.append({
                "timestamp": timestamp,
                "value": value,
                "metric_type": metric_type,
                "resource_labels": resource_labels,
                "metric_labels": metric_labels
            })
    return sorted(normalized_points, key=lambda p: p["timestamp"])

class MetricQueryRequest:
    project_id: str
    metric_type: str
    start_time: int
    end_time: int
    interval_seconds: Optional[int] = None
    filter_string: Optional[str] = None
    group_by: Optional[List[str]] = None
    reducer: Optional[Any] = None # monitoring_v3.Aggregation.Reducer
    aligner: Optional[Any] = None # monitoring_v3.Aggregation.Aligner

class MetricQueryResponse:
    points: List[Dict[str, Union[float, str, Dict[str, str]]]]
