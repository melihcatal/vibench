from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class TimeSeriesPoint(BaseModel):
    timestamp: str
    value: float


class MetricData(BaseModel):
    metric_name: str
    resource_labels: Dict[str, str]
    points: List[TimeSeriesPoint]


class AggregatedMetricData(BaseModel):
    metric_name: str
    aggregation: str
    value: float
    time_window: Dict[str, str]


class SafetyAnnotation(BaseModel):
    attribute: str
    score: float


class TranslationRequest(BaseModel):
    text: str
    target_language: str = "en"
    source_language: Optional[str] = None


class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_language: Optional[str] = None
