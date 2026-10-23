import dataclasses
from datetime import datetime
from typing import List, Dict, Any

@dataclasses.dataclass
class MetricQuery:
    metric_name: str
    start_time: datetime
    end_time: datetime
    dimensions: Dict[str, str] = dataclasses.field(default_factory=dict)

@dataclasses.dataclass
class MetricDataPoint:
    timestamp: datetime
    value: float

@dataclasses.dataclass
class MetricWindowResponse:
    metric_name: str
    data_points: List[MetricDataPoint]

@dataclasses.dataclass
class MetricAggregationResponse:
    metric_name: str
    start_time: datetime
    end_time: datetime
    statistic: str
    value: float

@dataclasses.dataclass
class MetricDimensionFilterResponse:
    metric_name: str
    filtered_data_points: Dict[str, List[MetricDataPoint]]

@dataclasses.dataclass
class MetricComparisonResponse:
    metric_name: str
    resource_a_data_points: List[MetricDataPoint]
    resource_b_data_points: List[MetricDataPoint]

@dataclasses.dataclass
class MetricSummary:
    metric_name: str
    summary_text: str

@dataclasses.dataclass
class AnnotationSafetyResult:
    text: str
    is_safe: bool
    reasons: List[str]

@dataclasses.dataclass
class TranslatedText:
    original_text: str
    translated_text: str
    target_locale: str

@dataclasses.dataclass
class ArchivedMetricSnapshot:
    snapshot_id: str
    storage_url: str
    timestamp: datetime
