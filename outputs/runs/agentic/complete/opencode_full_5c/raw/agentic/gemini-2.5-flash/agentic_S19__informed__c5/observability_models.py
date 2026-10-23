from datetime import datetime
from typing import Dict, Any, List

# Placeholder for request/response models and normalization


def normalize_time_series(time_series: List[Dict]) -> List[Dict]:
    normalized_data = []
    for series in time_series:
        metric_type = series.get("metric", {}).get("type", "unknown_metric")
        resource_type = series.get("resource", {}).get("type", "unknown_resource")
        points = series.get("points", [])
        for point in points:
            interval = point.get("interval", {})
            value = point.get("value", {})
            end_time = interval.get("endTime")

            normalized_point = {
                "metric_type": metric_type,
                "resource_type": resource_type,
                "end_time": end_time,
                "value": value.get("doubleValue")
                or value.get("int64Value")
                or value.get("stringValue")
                or value.get("boolValue"),
                "labels": {
                    "metric": series.get("metric", {}).get("labels", {}),
                    "resource": series.get("resource", {}).get("labels", {}),
                },
            }
            normalized_data.append(normalized_point)
    return normalized_data


def build_time_interval(start_time: datetime, end_time: datetime) -> Dict[str, Any]:
    return monitoring_v3.TimeInterval(
        end_time=end_time.isoformat() + "Z",
        start_time=start_time.isoformat() + "Z",
    )


def build_metric_filter(
    metric_name: str, resource_labels: Dict[str, str] = None
) -> str:
    filter_string = f'metric.type = "{metric_name}"'
    if resource_labels:
        for key, value in resource_labels.items():
            filter_string += f' AND resource.labels.{key} = "{value}"'
    return filter_string
