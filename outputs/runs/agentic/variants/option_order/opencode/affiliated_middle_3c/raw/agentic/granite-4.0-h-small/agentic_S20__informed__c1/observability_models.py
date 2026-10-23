from pydantic import BaseModel, Field

# Models for log payloads and API responses


class LogEntry(BaseModel):
    timestamp: str = Field(..., description="ISO8601 timestamp")
    level: str = Field(..., description="Log severity", alias="level")
    correlation_id: str = Field(None, description="Request identifier")
    text: str = Field(..., description="Human‑readable message")
    # Add any provider‑specific fields as needed


class LogWriteResponse(BaseModel):
    status: str = Field(..., description="Outcome")
    log_name: str = Field(None, description="Target log stream")
    request_id: str = Field(None, description="Provider‑generated request ID")


class QueryLogResponse(BaseModel):
    query: dict = Field(None, description="Original query parameters")
    entries: list[LogEntry] = Field([], description="Matched log entries")
    next_page_token: str = Field(None, description="Token for pagination")


class EmbeddingResponse(BaseModel):
    model_id: str = Field(..., description="Embedding model used")
    embeddings: list[list[float]] = Field([], description="Vector per input log")


class TranslationResponse(BaseModel):
    original: str = Field(..., description="Original log text")
    translated: str = Field(..., description="Translated text")
    target_locale: str = Field(..., description="ISO locale target")


class SafetyCheckResponse(BaseModel):
    safe: bool = Field(..., description="Whether the text passes the safety filter")
