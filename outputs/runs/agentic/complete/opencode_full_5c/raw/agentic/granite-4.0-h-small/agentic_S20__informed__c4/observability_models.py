from pydantic import BaseModel, Field
from datetime import datetime


class LogEvent(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message: str
    severity: str = Field(
        ..., description="Log severity level, e.g., info, error, warning"
    )
    correlationId: str | None = None
    # Add any provider‑specific fields here if needed.


class QueryFilter(BaseModel):
    severity: str | None = None
    startTime: datetime | None = None
    endTime: datetime | None = None
    # Provider‑specific filter keys can be added as needed.


class FetchFilter(BaseModel):
    # Example filter for field‑value matching (adjust key names per provider)
    field: str | None = None
    value: str | None = None

    class Config:
        extra = "allow"


class LogResult(BaseModel):
    logs: list[dict]
    total: int
    # Provider‑specific response fields can be added here.
