from google.cloud import monitoring_v3
from datetime import datetime, timedelta
from observability_client import ObservabilityClient
from observability_models import MetricStats

def aggregate_metric_stats(metric_name: str, hours: int = 1) -> MetricStats:
    client = ObservabilityClient()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    
    interval = monitoring_v3.TimeInterval(
        end_time=end_time,
        start_time=start_time
    )
    
    query = f"
        fetch gauge
        | metric 'custom.googleapis.com/{metric_name}'
        | group_by [resource.project_id], [value_mean: mean(value.value)]
        | every {hours * 60}s
    "
    
    result = client.client.query_time_series(name=client.project_name, query=query)
    points = list(result)
    
    if not points:
        return MetricStats(count=0, mean=0.0, min=0.0, max=0.0, sum=0.0)
    
    values = [float(point.value.double_value) for point in points[0].points]
    return MetricStats(
        count=len(values),
        mean=sum(values) / len(values),
        min=min(values),
        max=max(values),
        sum=sum(values)
    )