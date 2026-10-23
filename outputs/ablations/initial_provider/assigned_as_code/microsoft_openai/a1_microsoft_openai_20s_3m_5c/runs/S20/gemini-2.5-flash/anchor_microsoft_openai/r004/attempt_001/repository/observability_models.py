from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class LogEvent:
    TimeGenerated: str
    message: str
    severity: str
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CorrelatedLogEvent:
    TimeGenerated: str
    message: str
    correlation_id: str
    severity: str
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LogQueryRequest:
    workspace_id: str
    query: str
    timespan: str
    # Add other query parameters as needed

@dataclass
class LogQueryResult:
    timestamp: datetime
    message: str
    severity: str
    # Add other relevant fields from query results

@dataclass
class IncidentSummaryRequest:
    log_entries: List[LogQueryResult]

@dataclass
class IncidentSummaryResponse:
    summary: str

@dataclass
class TextSafetyRequest:
    text: str

@dataclass
class TextSafetyResponse:
    is_safe: bool
    reasons: List[str]

@dataclass
class TranslateRequest:
    text: str
    target_locale: str

@dataclass
class TranslateResponse:
    translated_text: str

@dataclass
class EmbeddingRequest:
    text: str

@dataclass
class EmbeddingResponse:
    embedding: List[float]
