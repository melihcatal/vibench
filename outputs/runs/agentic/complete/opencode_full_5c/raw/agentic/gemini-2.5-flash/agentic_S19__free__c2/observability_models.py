from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class MetricQuery:
    project_id: str
    metric_type: str
    interval_end_time: str
    interval_start_time: str
    filter: str = field(default="")
    aggregation_period_seconds: int = field(default=60)
    group_by_fields: List[str] = field(default_factory=list)
    view: int = field(default=1)  # 1 for FULL, 0 for HEADERS


@dataclass
class TimeSeriesPoint:
    value: Any
    timestamp: str


@dataclass
class TimeSeries:
    metric: Dict[str, Any]
    resource: Dict[str, Any]
    points: List[TimeSeriesPoint]


@dataclass
class MetricQueryResponse:
    time_series: List[TimeSeries]


@dataclass
class TranslatedText:
    translated_text: str
    detected_language_code: str


@dataclass
class DocumentSentiment:
    score: float
    magnitude: float


@dataclass
class Entity:
    name: str
    type: int
    salience: float
    sentiment: DocumentSentiment


@dataclass
class AnalyzeContentResponse:
    sentiment: DocumentSentiment
    entities: List[Entity]
