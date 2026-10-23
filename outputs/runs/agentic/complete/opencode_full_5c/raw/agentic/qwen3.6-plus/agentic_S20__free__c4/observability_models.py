import uuid
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class StructuredLogEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    message: str
    level: str = "info"
    service: str = "default-service"
    source: str = "python-app"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    custom_attributes: dict = Field(default_factory=dict)


class CorrelatedLogEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    message: str
    level: str = "info"
    source: str = "python-app"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    custom_attributes: dict = Field(default_factory=dict)


class LogWriteResponse(BaseModel):
    status: str
    event_id: str
    timestamp: str
    service: str


class CorrelatedLogWriteResponse(BaseModel):
    status: str
    correlation_id: str
    events_written: int
    events: list[dict]
    service: str


class ErrorLogQuery(BaseModel):
    service: str
    severity: str
    hours_back: int
    source: str | None = None


class ErrorLogEntry(BaseModel):
    event_id: str
    timestamp: str
    message: str
    level: str
    service: str
    source: str
    attributes: dict


class ErrorLogQueryResponse(BaseModel):
    query: ErrorLogQuery
    total_found: int
    entries: list[ErrorLogEntry]
    queried_at: str


class LogFetchParams(BaseModel):
    service: str
    field_filters: dict[str, str]
    hours_back: int
    limit: int
    sort_order: str = "desc"


class LogEntry(BaseModel):
    event_id: str
    timestamp: str
    message: str
    level: str
    service: str
    source: str
    attributes: dict


class LogFetchResponse(BaseModel):
    params: LogFetchParams
    total_found: int
    entries: list[LogEntry]
    fetched_at: str


class IncidentSummary(BaseModel):
    correlation_id: str | None = None
    service: str
    time_range: str
    total_errors: int
    error_categories: dict[str, int]
    affected_sources: list[str]
    top_messages: list[str]
    summary_text: str
    generated_at: str


class TextSafetyResult(BaseModel):
    text: str
    is_safe: bool
    flags: list[str]
    categories: dict[str, float]
    model_used: str


class TranslationResult(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    model_used: str


class EmbeddingResult(BaseModel):
    text: str
    embedding: list[float]
    model_used: str
    dimensions: int
