from datetime import datetime, timedelta
from typing import Dict, List
from observability_client import ObservabilityClient
from observability_models import MetricSeries, MetricStats

def summarize_metric_trends(metric_name: str, hours: int = 24) -> Dict:
    client = ObservabilityClient()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    
    interval = {
        "endTime": end_time.isoformat() + "Z",
        "startTime": start_time.isoformat() + "Z"
    }
    
    query = f"
        fetch gauge
        | metric 'custom.googleapis.com/{metric_name}'
        | group_by [resource.project_id], [value_mean: mean(value.value)]
        | every 3600s
        | group_by [], [value_mean_mean: mean(value_mean)]
    "
    
    result = client.client.query_time_series(name=client.project_name, query=query)
    points = list(result)
    
    if not points:
        return {"trend": "stable", "anomalies": [], "stats": MetricStats(count=0, mean=0.0, min=0.0, max=0.0, sum=0.0)}
    
    values = [float(point.value.double_value) for point in points[0].points]
    stats = MetricStats(
        count=len(values),
        mean=sum(values) / len(values),
        min=min(values),
        max=max(values),
        sum=sum(values)
    )
    
    trend = "stable"
    if len(values) >= 3:
        slope = (values[-1] - values[0]) / len(values)
        trend = "increasing" if slope > 0.1 else "decreasing" if slope < -0.1 else "stable"
    
    anomalies = []
    mean = stats.mean
    std_dev = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5
    for i, val in enumerate(values):
        if abs(val - mean) > 2 * std_dev:
            anomalies.append({
                "timestamp": (start_time + timedelta(hours=i)).isoformat(),
                "value": val,
                "expected_range": [mean - 2 * std_dev, mean + 2 * std_dev]
            })
    
    return {
        "trend": trend,
        "anomalies": anomalies,
        "stats": stats
    }