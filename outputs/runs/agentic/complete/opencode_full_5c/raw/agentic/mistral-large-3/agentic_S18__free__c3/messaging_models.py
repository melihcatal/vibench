from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class MessagePayload(BaseModel):
    """Represents a normalized message payload."""

    id: str = Field(..., description="Unique message identifier")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    content: Dict[str, Any] = Field(default_factory=dict, description="Message content")
    attributes: Dict[str, str] = Field(
        default_factory=dict, description="Message attributes"
    )


class BatchPublishRequest(BaseModel):
    """Request model for batch publishing messages."""

    messages: List[MessagePayload] = Field(
        ..., description="List of messages to publish"
    )


class BatchPublishResponse(BaseModel):
    """Response model for batch publishing messages."""

    message_ids: List[str] = Field(..., description="List of published message IDs")


class DeadLetterMessage(BaseModel):
    """Represents a message sent to dead-letter with error details."""

    original_message: MessagePayload = Field(
        ..., description="Original message payload"
    )
    error_details: str = Field(..., description="Error details")
    error_timestamp: str = Field(..., description="ISO 8601 error timestamp")


class ConsumeResponse(BaseModel):
    """Response model for consuming a message."""

    message: Optional[MessagePayload] = Field(None, description="Consumed message")
    success: bool = Field(False, description="Whether consumption was successful")
