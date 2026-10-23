from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class MetricDataPoint:
    timestamp: datetime
    value: float
    resource_labels: Dict[str, str]


@dataclass
class MetricQueryRequest:
    metric_name: str
    hours: int = 1


@dataclass
class MetricStatsRequest:
    metric_name: str
    window_hours: int = 1


@dataclass
class MetricStatsResponse:
    metric_name: str
    window_hours: int
    stats: List[Dict]


@dataclass
class DimensionFilterRequest:
    metric_name: str
    dimension_filters: Dict[str, str]
    window_hours: int = 1


@dataclass
class MetricComparisonRequest:
    metric_name: str
    filters_a: Dict[str, str]
    filters_b: Dict[str, str]
    window_hours: int = 1


@dataclass
class MetricComparisonResponse:
    metric_name: str
    window_hours: int
    series_a: List[Dict]
    series_b: List[Dict]


@dataclass
class MetricSummaryRequest:
    metric_name: str
    window_hours: int = 24
    locale: str = "en-US"


@dataclass
class MetricSummaryResponse:
    summary_text: str
    anomalies: List[Dict]


@dataclass
class AnnotationSafetyRequest:
    text: str
    locale: str = "en-US"


@dataclass
class AnnotationSafetyResponse:
    is_safe: bool
    violations: List[Dict]


@dataclass
class TranslationRequest:
    text: str
    target_locale: str


@dataclass
class TranslationResponse:
    translated_text: str


@dataclass
class MetricsExportRequest:
    metric_names: List[str]
    window_hours: int = 24
    export_format: str = "json"


@dataclass
class MetricsExportResponse:
    archive_path: str