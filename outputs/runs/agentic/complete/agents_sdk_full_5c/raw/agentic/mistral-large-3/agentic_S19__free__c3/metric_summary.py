from datetime import datetime, timedelta
import os
from google.cloud import monitoring_v3
from google.cloud.monitoring_dashboard import v1
from observability_client import get_monitoring_client


def summarize_metric_trends(metric_type: str, hours: int = 24) -> dict:
    client = get_monitoring_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    
    query = (
        f'fetch gcp_metric :: {metric_type} '
        f'| within {hours}h '
        f'| every {max(1, hours // 24)}m '
        f'| group_by [resource.project_id, resource.instance_id], [value_mean: mean(value.double_value)]'
    )
    
    result = client.query_time_series(
        name=f"projects/{project_id}",
        query=query
    )
    
    trends = {}
    for series in result.time_series:
        resource_id = series.resource.labels.get("instance_id", "unknown")
        values = [point.value.double_value for point in series.points]
        trends[resource_id] = {
            "mean": sum(values) / len(values) if values else 0.0,
            "trend": "rising" if len(values) > 1 and values[-1] > values[0] else "falling" if len(values) > 1 else "stable",
            "anomalies": _detect_anomalies(values)
        }
    
    return {
        "metric_type": metric_type,
        "window_hours": hours,
        "trends": trends
    }


def _detect_anomalies(values: list[float], threshold: float = 2.0) -> list[dict]:
    if len(values) < 3:
        return []
    
    mean = sum(values) / len(values)
    stddev = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5
    
    anomalies = []
    for i, value in enumerate(values):
        if stddev > 0 and abs(value - mean) > threshold * stddev:
            anomalies.append({
                "index": i,
                "value": value,
                "mean": mean,
                "stddev": stddev
            })
    
    return anomalies