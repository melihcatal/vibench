from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class MetricWindowRequest:
    metric_type: str
    start_time: Any
    end_time: Any
    filter_expression: Optional[str] = None


@dataclass
class MetricAggregateRequest:
    metric_type: str
    start_time: Any
    end_time: Any
    alignment_period_seconds: int = 60
    reducer: str = "REDUCE_MEAN"


@dataclass
class MetricFilterRequest:
    metric_type: str
    start_time: Any
    end_time: Any
    dimension_filter: Dict[str, str]


@dataclass
class MetricCompareRequest:
    metric_type: str
    start_time: Any
    end_time: Any
    left_filter: str
    right_filter: str


def normalize_point(point: Any) -> Dict[str, Any]:
    metric = getattr(point, "metric", None)
    resource = getattr(point, "resource", None)
    interval = getattr(point, "interval", None)
    value = getattr(point, "value", None)
    return {
        "metric": dict(metric.labels) if metric else {},
        "resource": dict(resource.labels) if resource else {},
        "interval": {
            "start_time": getattr(interval, "start_time", None),
            "end_time": getattr(interval, "end_time", None),
        },
        "value": value,
    }


def dataclass_to_dict(item: Any) -> Dict[str, Any]:
    return asdict(item)


def series_to_list(series: List[Any]) -> List[Dict[str, Any]]:
    return [normalize_point(point) for point in series]
