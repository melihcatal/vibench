from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class MetricWindowRequest:
    metric_name: str
    start_time: str
    end_time: str
    step: Optional[str] = None
    dimensions: Optional[Dict[str, str]] = None


@dataclass
class AggregatedMetricRequest:
    metric_name: str
    start_time: str
    end_time: str
    statistic: str
    dimensions: Optional[Dict[str, str]] = None


@dataclass
class MetricComparisonRequest:
    metric_name: str
    start_time: str
    end_time: str
    left_filter: Dict[str, str]
    right_filter: Dict[str, str]


@dataclass
class MetricSummaryRequest:
    metric_name: str
    start_time: str
    end_time: str
    lookback_points: int = 20


@dataclass
class MetricAnnotationRequest:
    text: str
    locale: Optional[str] = None


@dataclass
class MetricsExportRequest:
    bucket: str
    object_name: str
    payload: Dict[str, Any]


def normalize_dimensions(dimensions: Optional[Dict[str, str]]) -> Dict[str, str]:
    if not dimensions:
        return {}
    return {
        str(k): str(v) for k, v in dimensions.items() if k is not None and v is not None
    }


def normalize_datapoints(datapoints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for point in datapoints:
        item = dict(point)
        if "value" in item:
            try:
                item["value"] = float(item["value"])
            except (TypeError, ValueError):
                pass
        normalized.append(item)
    return normalized
