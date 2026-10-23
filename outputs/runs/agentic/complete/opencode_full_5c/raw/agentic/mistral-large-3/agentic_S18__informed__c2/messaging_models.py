from typing import Dict, Any, Optional, TypedDict
from dataclasses import dataclass


class PublishRequest(TypedDict):
    """Request structure for publishing a message."""

    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]]


class PublishResponse(TypedDict):
    """Response structure for publishing a message."""

    message_id: str


class ConsumeResponse(TypedDict):
    """Response structure for consuming a message."""

    data: Dict[str, Any]
    message_id: Optional[str]
    attributes: Optional[Dict[str, str]]


def normalize_message_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes message data by ensuring it is JSON-serializable.

    Args:
        data: The message data to normalize.

    Returns:
        Dict[str, Any]: The normalized message data.
    """
    return {
        key: str(value)
        if not isinstance(value, (str, int, float, bool, dict, list))
        else value
        for key, value in data.items()
    }
