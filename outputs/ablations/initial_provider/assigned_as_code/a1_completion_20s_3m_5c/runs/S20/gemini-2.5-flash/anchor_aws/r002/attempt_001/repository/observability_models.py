from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class LogEvent:
    timestamp: int
    message: str

@dataclass
class LogGroupConfig:
    log_group_name: str
    log_stream_name: str
    region_name: str

@dataclass
class FilteredLogEntry:
    timestamp: int
    message: str
    log_stream_name: str
    log_group_name: str

@dataclass
class LogQuery:
    query_string: str
    start_time: int
    end_time: int
    limit: Optional[int] = None

@dataclass
class IncidentSummaryRequest:
    error_logs: List[str]

@dataclass
class SafetyCheckRequest:
    text_content: str

@dataclass
class TranslationRequest:
    text_content: str
    target_language: str

@dataclass
class EmbeddingRequest:
    text_content: str
