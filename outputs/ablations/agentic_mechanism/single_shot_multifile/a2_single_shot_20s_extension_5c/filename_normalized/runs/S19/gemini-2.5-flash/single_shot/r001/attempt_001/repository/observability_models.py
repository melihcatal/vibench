from typing import List, Dict, Any, Optional
from datetime import datetime

class MetricDatapoint:
    def __init__(self, timestamp: datetime, value: float, unit: Optional[str] = None, labels: Optional[Dict[str, str]] = None):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit
        self.labels = labels if labels is not None else {}

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "unit": self.unit,
            "labels": self.labels
        }

class MetricTimeSeries:
    def __init__(self, metric_name: str, datapoints: List[MetricDatapoint], dimensions: Optional[Dict[str, str]] = None):
        self.metric_name = metric_name
        self.datapoints = datapoints
        self.dimensions = dimensions if dimensions is not None else {}

    def to_dict(self):
        return {
            "metric_name": self.metric_name,
            "datapoints": [dp.to_dict() for dp in self.datapoints],
            "dimensions": self.dimensions
        }

class MetricSummaryResult:
    def __init__(self, summary_text: str, detected_anomalies: List[Dict[str, Any]] = None):
        self.summary_text = summary_text
        self.detected_anomalies = detected_anomalies if detected_anomalies is not None else []

    def to_dict(self):
        return {
            "summary_text": self.summary_text,
            "detected_anomalies": self.detected_anomalies
        }

class SafetyCheckResult:
    def __init__(self, is_safe: bool, details: Optional[Dict[str, Any]] = None):
        self.is_safe = is_safe
        self.details = details if details is not None else {}

    def to_dict(self):
        return {
            "is_safe": self.is_safe,
            "details": self.details
        }

class TranslatedText:
    def __init__(self, original_text: str, translated_text: str, source_lang: str, target_lang: str):
        self.original_text = original_text
        self.translated_text = translated_text
        self.source_lang = source_lang
        self.target_lang = target_lang

    def to_dict(self):
        return {
            "original_text": self.original_text,
            "translated_text": self.translated_text,
            "source_lang": self.source_lang,
            "target_lang": self.target_lang
        }
