from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class MessageAttributes(BaseModel):
    """
    Model for Pub/Sub message attributes.
    """

    message_id: Optional[str] = Field(
        default=None, description="Unique identifier for the message"
    )
    source: Optional[str] = Field(default=None, description="Source of the message")
    timestamp: Optional[str] = Field(
        default=None, description="Timestamp of the message"
    )


class PubSubMessage(BaseModel):
    """
    Model for a Pub/Sub message.
    """

    data: Dict[str, Any] = Field(..., description="The message payload")
    attributes: MessageAttributes = Field(
        default_factory=MessageAttributes, description="Message attributes"
    )

    class Config:
        arbitrary_types_allowed = True


class BatchPublishRequest(BaseModel):
    """
    Model for a batch publish request.
    """

    messages: List[PubSubMessage] = Field(
        ..., description="List of messages to publish"
    )


class BatchPublishResponse(BaseModel):
    """
    Model for a batch publish response.
    """

    message_ids: List[str] = Field(..., description="List of published message IDs")


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a message payload to ensure consistent structure.

    Args:
        payload: Dictionary containing the message payload.

    Returns:
        Dict[str, Any]: Normalized payload.
    """
    return {
        "content": payload.get("content", ""),
        "metadata": payload.get("metadata", {}),
    }
