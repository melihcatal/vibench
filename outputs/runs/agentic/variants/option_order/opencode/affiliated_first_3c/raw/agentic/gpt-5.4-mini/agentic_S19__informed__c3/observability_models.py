from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class MetricWindowRequest:
    namespace: str
    metric_name: str
    start_time: Any
    end_time: Any
    period: int = 60
    statistic: str = 'Average'
    dimensions: Optional[Dict[str, str]] = None


@dataclass
class MetricSeriesPoint:
    timestamp: Any
    value: float
    dimensions: Optional[Dict[str, str]] = None


@dataclass
class MetricSeriesResponse:
    metric_name: str
    namespace: str
    points: List[MetricSeriesPoint]
    statistics: Optional[Dict[str, float]] = None


def normalize_dimensions(dimensions: Optional[Dict[str, str]]) -> List[Dict[str, str]]:
    return [{'Name': k, 'Value': str(v)} for k, v in (dimensions or {}).items()]


def series_from_datapoints(metric_name: str, namespace: str, datapoints: List[Dict[str, Any]]) -> MetricSeriesResponse:
    points = [MetricSeriesPoint(timestamp=dp.get('Timestamp'), value=float(dp.get('Average', dp.get('Value', 0.0)))) for dp in datapoints]
    return MetricSeriesResponse(metric_name=metric_name, namespace=namespace, points=points)
