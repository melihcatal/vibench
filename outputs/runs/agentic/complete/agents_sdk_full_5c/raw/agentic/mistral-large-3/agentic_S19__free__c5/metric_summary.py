from google.cloud import monitoring_v3
from google.api import metric_service_v3
from observability_client import get_monitoring_client
from observability_models import MetricQueryRequest
from datetime import datetime, timedelta
import numpy as np

def detect_anomalies(values: list[float], threshold: float = 2.0) -> list[bool]:
    if len(values) < 3:
        return [False] * len(values)
    mean = np.mean(values)
    std = np.std(values)
    return [abs(v - mean) > threshold * std for v in values]

def summarize_metric_trends(request: MetricQueryRequest) -> dict:
    client = get_monitoring_client()
    project_name = f"projects/{request.project_id}"
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=request.hours)
    
    query_request = {
        "name": project_name,
        "filter": f'metric.type="{request.metric_type}"',
        "interval": {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(end_time.timestamp())}
        },
        "aggregation": {
            "alignment_period": {"seconds": 60},
            "per_series_aligner": metric_service_v3.Aggregation.Aligner.ALIGN_MEAN
        }
    }
    
    values = []
    for series in client.list_time_series(request=query_request):
        for point in series.points:
            values.append(float(point.value.double_value))
    
    anomalies = detect_anomalies(values)
    
    return {
        "metric_type": request.metric_type,
        "trend": "increasing" if values[-1] > values[0] else "decreasing" if values[-1] < values[0] else "stable",
        "anomaly_count": sum(anomalies),
        "recent_value": values[-1] if values else 0
    }