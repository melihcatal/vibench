from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class MetricPoint(BaseModel):
    timestamp: int
    value: float


class MetricSeries(BaseModel):
    metric_name: str
    points: List[MetricPoint]
    tags: Optional[Dict[str, str]] = None


class MetricStatistics(BaseModel):
    metric_name: str
    avg: float
    max: float
    min: float
    sum: float
    tags: Optional[Dict[str, str]] = None


class AnnotationSafetyResult(BaseModel):
    text: str
    is_safe: bool
    scores: Dict[str, float]


class TranslationResult(BaseModel):
    original_text: str
    translated_text: str
    target_locale: str
    source_locale: str
