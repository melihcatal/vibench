import time
from typing import List
from observability_client import get_datadog_client
from observability_models import MetricSeries, MetricDataPoint

def query_metric_window(metric_name: str, hours: int = 1) -> List[MetricSeries]:
    client = get_datadog_client()
    
    to_ts = int(time.time())
    from_ts = to_ts - (hours * 3600)
    
    query = f"avg:{metric_name}{{*} by {{*}}}"
    
    try:
        data = client.query_metrics(query, from_ts, to_ts)
        
        result_series = []
        if data.get("status") == "ok":
            for series in data.get("series", []):
                points = [MetricDataPoint(timestamp=int(p[0]/1000), value=p[1]) for p in series.get("pointlist", []) if p[1] is not None]
                metric_series = MetricSeries(
                    metric_name=series.get("metric"),
                    points=points,
                    tags=series.get("tag_set")
                )
                result_series.append(metric_series)
        return result_series
    except Exception as e:
        print(f"Error querying Datadog: {e}")
        return []
