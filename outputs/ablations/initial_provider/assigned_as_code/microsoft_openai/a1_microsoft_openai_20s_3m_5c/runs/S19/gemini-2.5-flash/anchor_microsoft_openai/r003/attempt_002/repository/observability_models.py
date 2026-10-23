from typing import List, Dict, Any, Optional
from datetime import datetime

class MetricQueryPayload:
    metric_name: str
    start_time: datetime
    end_time: datetime
    project_id: str
    interval_seconds: Optional[int] = None
    filter: Optional[str] = None
    aggregation_aligner: Optional[str] = None
    aggregation_reducer: Optional[str] = None
    group_by: Optional[List[str]] = None

class MetricQueryResult:
    points: List[Dict[str, Any]]

class AnnotationSafetyPayload:
    text: str
    project_id: str

class AnnotationSafetyResult:
    safe: bool
    reasons: List[str]

class DashboardNoteTranslatePayload:
    text: str
    target_language: str
    project_id: str

class DashboardNoteTranslateResult:
    translated_text: str

class MetricsExportArchivePayload:
    metric_data: Dict[str, Any]
    bucket_name: str
    destination_blob_name: str

class MetricsExportArchiveResult:
    success: bool
    uri: str
