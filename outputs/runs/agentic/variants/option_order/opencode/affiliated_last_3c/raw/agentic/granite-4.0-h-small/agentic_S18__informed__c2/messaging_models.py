# messaging_models.py
# HELPER: Payload/request/response structures for the messaging scenario

from pydantic import BaseModel, Field, validator


class Event(BaseModel):
    """Core event payload sent to SNS and consumed from SQS."""

    event_id: str = Field(..., description="Unique identifier for the event")
    data: dict = Field(..., description="Arbitrary data carried by the event")
    timestamp: str = Field(
        ...,
        format="date-time",
        description="ISO8601 timestamp when the event was created",
    )

    @validator("event_id")
    def validate_uuid(cls, v) -> str:
        # Simple check that it looks like a UUID (not full validation)
        if "-" not in v:
            raise ValueError("event_id should be a UUID-like string containing hyphens")
        return v


class MessagePayload(BaseModel):
    """Helper wrapper for messages that include metadata for processing pipelines."""

    source: str = Field("sns", description="Origin service of the message")
    payload: Event = Field(..., description="The actual event payload")
    attempt: int = Field(1, description="Processing attempt count")

    def to_dict(self) -> dict:
        """Return a plain dict ready for JSON serialization."""
        return {
            "source": self.source,
            "attempt": self.attempt,
            "payload": self.payload.dict(),
        }


class ErrorResponse(BaseModel):
    """Structured error response used in later-step files."""

    type: str = Field("messaging_error", description="Error category")
    code: str
    message: str
    details: dict = Field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


if __name__ == "__main__":
    # Demo validation
    ev = Event(
        event_id="123e4567-e89b-12d3-a456-426614174000",
        data={"key": "value"},
        timestamp="2025-08-01T12:00:00Z",
    )
    print("Valid Event:", ev.json())
