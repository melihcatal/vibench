from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class LogEvent:
    message: str
    severity: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CorrelatedLogEvent(LogEvent):
    correlation_id: str

@dataclass
class LogQuery:
    workspace_id: str
    query: str
    timespan: str # e.g., "PT1H" for 1 hour, "P1D" for 1 day
    
@dataclass
class QueryResult:
    tables: List[Dict[str, Any]]

@dataclass
class IncidentSummary:
    summary_text: str

@dataclass
class SafetyCheckResult:
    unsafe_content_found: bool
    categories: Dict[str, Any]

@dataclass
class TranslatedMessage:
    translated_text: str
    target_locale: str

@dataclass
class LogEmbedding:
    embedding_vector: List[float]
