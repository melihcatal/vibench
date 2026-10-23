import time
from typing import Optional
from observability_client import get_datadog_client
from observability_models import MetricStatistics

def get_aggregate_metric_stats(metric_name: str, aggregation: str = "avg", hours: int = 24) -> Optional[MetricStatistics]:
    client = get_datadog_client()
    
    to_ts = int(time.time())
    from_ts = to_ts - (hours * 3600)
    
    query = f"{aggregation}:{metric_name}{{*} by {{*}}}"
    
    try:
        data = client.query_metrics(query, from_ts, to_ts)
        
        if data.get("status") == "ok" and data.get("series"):
            # This provides a simple aggregation over the points in the first returned series
            series = data["series"][0]
            
            points = [p[1] for p in series.get("pointlist", []) if p[1] is not None]
            if not points:
                return None

            aggregated_value = 0
            if aggregation == "avg":
                aggregated_value = sum(points) / len(points)
            elif aggregation == "max":
                aggregated_value = max(points)
            elif aggregation == "min":
                aggregated_value = min(points)
            elif aggregation == "sum":
                aggregated_value = sum(points)
            else: # Unsupported aggregation
                return None

            return MetricStatistics(
                metric_name=series.get("metric"),
                statistic=aggregation,
                value=aggregated_value,
                tags=series.get("tag_set")
            )
        return None
    except Exception as e:
        print(f"Error querying Datadog for aggregation: {e}")
        return None
