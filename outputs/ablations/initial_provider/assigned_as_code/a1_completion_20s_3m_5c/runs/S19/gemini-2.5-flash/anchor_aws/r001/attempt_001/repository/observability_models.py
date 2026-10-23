from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class MetricQuery:
    metric_name: str
    start_time: int
    end_time: int
    namespace: str
    dimensions: Dict[str, str]
    period_seconds: int = 60
    statistics: List[str] = None

@dataclass
class MetricDatapoint:
    timestamp: float
    value: float

@dataclass
class MetricDataResult:
    label: str
    datapoints: List[MetricDatapoint]

@dataclass
class AggregatedMetricStats:
    minimum: float
    maximum: float
    average: float
    sum: float
    sample_count: float

@dataclass
class AnnotationSafetyCheckResult:
    unsafe_content_found: bool
    details: str

@dataclass
class TranslatedText:
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class ArchiveResult:
    archive_url: str
    status: str
