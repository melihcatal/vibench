from pydantic import BaseModel, Field

# Request model for publishing an event


class PublishRequest(BaseModel):
    payload: dict = Field(..., description="Application-specific message payload")
    message_id: str = Field(
        None, description="Optional unique identifier for the message"
    )
    attributes: dict = Field(
        None, description="Optional custom attributes to attach to the message"
    )


# Basic response wrapper used by the publish helpers
class PublishResponse(BaseModel):
    success: bool = True
    message_id: str = None
    provider_response: dict = None


class ConsumeRequest(BaseModel):
    subscription: str = Field(..., description="Topic/queue name to consume from")
    max_messages: int = Field(
        1, gt=0, description="Maximum number of messages to fetch"
    )
    wait_seconds: int = Field(10, gt=0, description="Longest poll duration in seconds")


# Response wrapper for batch publishing (list of futures or IDs)
class BatchPublishResponse(BaseModel):
    published_ids: list[str] = []
    errors: list[dict] = []


# Payload model for storing processed message records


class MessageRecord(BaseModel):
    original: dict = Field(..., description="Raw message as received")
    processed: dict = Field(None, description="Normalized or transformed content")
    status: str = Field(
        "received", description="Processing status: received|processed|dead_lettered"
    )
    error: str = Field(None, description="Error message if processing failed")
