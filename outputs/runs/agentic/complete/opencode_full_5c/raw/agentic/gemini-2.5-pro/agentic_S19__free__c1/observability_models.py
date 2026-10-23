from pydantic import BaseModel
from typing import List, Dict, Any


class TimeSeriesPoint(BaseModel):
    timestamp: str
    value: float


class MetricTimeSeries(BaseModel):
    metric_name: str
    dimensions: Dict[str, str]
    points: List[TimeSeriesPoint]


class AggregatedMetricStats(BaseModel):
    metric_name: str
    dimensions: Dict[str, str]
    statistic: str
    value: float


class AnnotationSafetyResult(BaseModel):
    text: str
    scores: Dict[str, float]
    safe: bool


class TranslatedText(BaseModel):
    original_text: str
    translated_text: str
    target_language: str
