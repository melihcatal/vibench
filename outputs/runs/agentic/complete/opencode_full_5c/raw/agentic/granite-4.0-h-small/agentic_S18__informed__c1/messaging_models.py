import os
from typing import TypedDict

# Request model for publishing
PublishRequest = TypedDict(
    "PublishRequest",
    {
        "topic": str,
        "payload": dict,
    },
)

# Response model for publishing (status and optional metadata)
PublishResponse = TypedDict(
    "PublishResponse",
    {
        "status": str,
        "message_id": str,
        "error": str,
    },
)

# Request model for consuming a single message
ConsumeRequest = TypedDict(
    "ConsumeRequest",
    {
        "subscription": str,
    },
)

# Response model for a consumed message
ConsumeResponse = TypedDict(
    "ConsumeResponse",
    {
        "status": str,
        "message": dict,
        "error": str,
    },
)

# Normalization helper to standardize message payload across providers
NORMALIZED_MESSAGE = TypedDict(
    "NormalizedMessage",
    {
        "event_id": str,
        "timestamp": str,
        "payload": dict,
    },
)
