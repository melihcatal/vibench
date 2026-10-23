from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass
class MetricPoint:
    value: float
    timestamp: datetime

@dataclass
class TimeSeries:
    metric_type: str
    resource_labels: Dict[str, str]
    points: List[MetricPoint]

@dataclass
class MetricQueryRequest:
    project_id: str
    metric_type: str
    end_time: datetime
    duration_minutes: int
    dimension_filters: Optional[Dict[str, str]] = None
    aggregation_period_seconds: Optional[int] = None
    alignment_period_seconds: Optional[int] = None

@dataclass
class MetricSummaryRequest:
    project_id: str
    metric_type: str
    end_time: datetime
    duration_minutes: int
    context_info: Optional[str] = None

@dataclass
class TextAnnotationRequest:
    text: str
    project_id: str

@dataclass
class TranslationRequest:
    text: str
    target_language_code: str
    project_id: str
    source_language_code: Optional[str] = None

@dataclass
class ExportArchiveRequest:
    bucket_name: str
    file_name: str
    data_content: str
    project_id: str
