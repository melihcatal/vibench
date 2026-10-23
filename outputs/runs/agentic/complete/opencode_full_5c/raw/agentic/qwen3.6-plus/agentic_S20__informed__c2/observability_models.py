import os
import json
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from enum import Enum


class LogSeverity(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"


@dataclass
class StructuredLogEvent:
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    severity: str = LogSeverity.INFO.value
    message: str = ""
    service: str = ""
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = ""
    attributes: dict = field(default_factory=dict)

    def to_sls_log_content(self) -> list[tuple[str, str]]:
        content = [
            ("timestamp", self.timestamp),
            ("severity", self.severity),
            ("message", self.message),
            ("service", self.service),
            ("correlation_id", self.correlation_id),
            ("request_id", self.request_id),
            ("source", self.source),
        ]
        for key, value in self.attributes.items():
            content.append(
                (
                    f"attr_{key}",
                    json.dumps(value) if not isinstance(value, str) else value,
                )
            )
        return content

    @classmethod
    def from_dict(cls, data: dict) -> "StructuredLogEvent":
        return cls(
            timestamp=data.get("timestamp", datetime.now(timezone.utc).isoformat()),
            severity=data.get("severity", LogSeverity.INFO.value),
            message=data.get("message", ""),
            service=data.get("service", ""),
            correlation_id=data.get("correlation_id", str(uuid.uuid4())),
            request_id=data.get("request_id", str(uuid.uuid4())),
            source=data.get("source", ""),
            attributes=data.get("attributes", {}),
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LogQueryResult:
    logs: list[dict] = field(default_factory=list)
    count: int = 0
    query_id: str = ""
    completed: bool = False
    progress: float = 0.0

    @classmethod
    def from_sls_response(cls, response: dict) -> "LogQueryResult":
        logs = []
        if isinstance(response, dict):
            raw_logs = response.get("logs", [])
            for log_entry in raw_logs:
                normalized = {}
                for key, value in log_entry.items():
                    normalized[key] = value
                logs.append(normalized)
            return cls(
                logs=logs,
                count=response.get("count", len(logs)),
                query_id=response.get("query_id", ""),
                completed=response.get("completed", True),
                progress=response.get("progress", 1.0),
            )
        return cls(logs=logs)

    def filter_by_severity(self, severity: str) -> list[dict]:
        return [
            log
            for log in self.logs
            if log.get("severity", "").upper() == severity.upper()
        ]

    def filter_by_time_range(self, start: str, end: str) -> list[dict]:
        filtered = []
        for log in self.logs:
            ts = log.get("timestamp", "")
            if start <= ts <= end:
                filtered.append(log)
        return filtered

    def filter_by_field(self, field_name: str, field_value: Any) -> list[dict]:
        return [log for log in self.logs if log.get(field_name) == field_value]


@dataclass
class SlsClientConfig:
    endpoint: str = ""
    access_key_id: str = ""
    access_key_secret: str = ""
    project: str = ""
    logstore: str = ""

    @classmethod
    def from_env(cls) -> "SlsClientConfig":
        endpoint = os.environ.get(
            "ALIBABA_SLS_ENDPOINT", "cn-hangzhou.log.aliyuncs.com"
        )
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID", "")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "")
        project = os.environ.get("ALIBABA_SLS_PROJECT", "default-log-project")
        logstore = os.environ.get("ALIBABA_SLS_LOGSTORE", "application-logs")
        return cls(
            endpoint=endpoint,
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            project=project,
            logstore=logstore,
        )


@dataclass
class IncidentFinding:
    log_entry: dict
    severity: str
    summary: str = ""
    translated_message: str = ""
    safety_flags: list[str] = field(default_factory=list)
    embedding: list[float] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "log_entry": self.log_entry,
            "severity": self.severity,
            "summary": self.summary,
            "translated_message": self.translated_message,
            "safety_flags": self.safety_flags,
            "embedding": self.embedding,
        }
