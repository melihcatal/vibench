from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class MetricPoint:
    timestamp: float
    value: float

@dataclass
class MetricSeries:
    name: str
    data: List[MetricPoint]
    dimensions: Dict[str, str]

def normalize_azure_metrics_result(azure_result: Any) -> List[MetricSeries]:
    normalized_series = []
    for metric in azure_result.metrics:
        for ts_data in metric.timeseries:
            points = []
            for point in ts_data.data:
                if point.average is not None:
                    points.append(MetricPoint(timestamp=point.timestamp.timestamp(), value=float(point.average)))
            
            dimensions = {}
            if ts_data.metadata:
                dimensions = {k: str(v) for k, v in ts_data.metadata.items()}
            
            normalized_series.append(MetricSeries(name=metric.name, data=points, dimensions=dimensions))
    return normalized_series
