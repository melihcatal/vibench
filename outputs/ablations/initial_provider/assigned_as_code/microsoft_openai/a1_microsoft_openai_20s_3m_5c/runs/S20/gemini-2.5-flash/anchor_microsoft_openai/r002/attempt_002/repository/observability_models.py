from typing import Dict, Any, List, Literal
from datetime import datetime, timezone

class LogEvent:
    def __init__(self, message: str, severity: str, timestamp_ms: int, properties: Dict[str, Any]):
        self.message = message
        self.severity = severity
        self.timestamp_ms = timestamp_ms
        self.properties = properties

    def to_azure_monitor_log(self) -> Dict[str, Any]:
        event = {
            "Message": self.message,
            "Severity": self.severity,
            "TimeGenerated": datetime.fromtimestamp(self.timestamp_ms / 1000, tz=timezone.utc).isoformat(),
        }
        event.update(self.properties)
        return event

class LogQueryRequest:
    def __init__(self, workspace_id: str, query: str, timespan: str = "PT1H"):
        self.workspace_id = workspace_id
        self.query = query
        self.timespan = timespan

class LogQueryResponse:
    def __init__(self, tables: List[Dict[str, Any]]):
        self.tables = tables

    def to_dict(self) -> Dict[str, Any]:
        return {"tables": self.tables}

class SummarizationRequest:
    def __init__(self, log_entries: List[str]):
        self.log_entries = log_entries

class SafetyCheckRequest:
    def __init__(self, text: str):
        self.text = text

class TranslationRequest:
    def __init__(self, text: str, target_language: str):
        self.text = text
        self.target_language = target_language

class EmbeddingRequest:
    def __init__(self, text: str):
        self.text = text
