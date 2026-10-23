from pydantic import BaseModel, Field, validator

class LogEntry(BaseModel):
    timestamp: str = Field(default_factory=datetime.datetime.utcnow().isoformat, description="ISO 8601 timestamp")
    resource_id: str = Field(..., description="Identifier for the originating resource")
    message: str = Field(..., description="Log message text")
    level: str = Field(..., description="Severity level (info, error, warn, etc.)")
    correlation_id: str = Field(default=None, description="Optional correlation identifier for grouping")
    tags: dict = Field(default_factory=dict, description="Optional key/value tags")

    @validator('level')
    def validate_level(cls, v):
        valid_levels = {"debug", "info", "warn", "error", "critical"}
        if v.lower() not in valid_levels:
            raise ValueError(f"Invalid level {v}. Must be one of {valid_levels}")
        return v.lower()

def normalize_log_entry(entry: dict) -> LogEntry:
    """Normalize raw dict from external source to LogEntry model."""
    return LogEntry.parse_obj(entry)
