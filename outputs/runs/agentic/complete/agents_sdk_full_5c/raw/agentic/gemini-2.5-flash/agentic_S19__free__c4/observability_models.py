import dataclasses
from typing import List, Dict, Any, Optional

@dataclasses.dataclass
class MetricDataPoint:
    metric_type: str
    value: float
    timestamp: str
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]

@dataclasses.dataclass
class MetricTimeSeries:
    resource_id: str
    points: List[MetricDataPoint]

@dataclasses.dataclass
class AggregatedMetricStat:
    metric_type: str
    value: float
    timestamp: str
    resource_labels: Dict[str, str]
    aggregation_type: str

@dataclasses.dataclass
class MetricSummary:
    metric_type: str
    trend: str
    anomaly_detected: bool
    summary_text: str

@dataclasses.dataclass
class TranslatedText:
    source_language_code: str
    target_language_code: str
    translated_text: str
    original_text: str

@dataclasses.dataclass
class ArchiveResult:
    blob_name: str
    bucket_name: str
    success: bool
    error_message: Optional[str] = None
