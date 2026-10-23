from typing import Dict, Any, List, Optional
from datetime import datetime

class LogEvent:
    def __init__(self, timestamp_ms: int, message: str, log_stream_name: str):
        self.timestamp_ms = timestamp_ms
        self.message = message
        self.log_stream_name = log_stream_name

class StructuredLogPayload:
    def __init__(self, event: Dict[str, Any], timestamp_ms: Optional[int] = None):
        self.event = event
        self.timestamp_ms = timestamp_ms

class LogQuery:
    def __init__(self, log_group_name: str, start_time: datetime, end_time: datetime, filter_pattern: Optional[str] = None, limit: int = 100):
        self.log_group_name = log_group_name
        self.start_time = start_time
        self.end_time = end_time
        self.filter_pattern = filter_pattern
        self.limit = limit

class QueryResult:
    def __init__(self, fields: List[Dict[str, str]], records: List[Dict[str, str]]):
        self.fields = fields
        self.records = records

class IncidentSummaryRequest:
    def __init__(self, error_logs: List[Dict[str, Any]]):
        self.error_logs = error_logs

class SafetyCheckRequest:
    def __init__(self, text: str):
        self.text = text

class TranslationRequest:
    def __init__(self, text: str, target_language_code: str):
        self.text = text
        self.target_language_code = target_language_code

class EmbeddingRequest:
    def __init__(self, text: List[str]):
        self.text = text
