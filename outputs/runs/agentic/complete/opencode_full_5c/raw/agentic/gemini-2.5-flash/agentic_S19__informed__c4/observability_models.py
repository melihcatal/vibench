from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class MetricQueryRequest:
    project_id: str
    metric_type: str
    end_time: str
    start_time: str
    interval_seconds: int = 60
    filter_string: str = ""
    group_by_fields: List[str] | None = None
    aggregator: str = "MEAN"


@dataclass
class MetricQueryResult:
    time: str
    value: float
    labels: Dict[str, str]


@dataclass
class MetricQueryResponse:
    metric_data: List[MetricQueryResult]


@dataclass
class MetricAnnotationSafetyRequest:
    text: str


@dataclass
class MetricAnnotationSafetyResponse:
    safe: bool
    score: float


@dataclass
class DashboardNoteTranslationRequest:
    text: str
    target_language: str


@dataclass
class DashboardNoteTranslationResponse:
    translated_text: str


@dataclass
class MetricExportArchiveRequest:
    bucket_name: str
    destination_blob_name: str
    data: str
