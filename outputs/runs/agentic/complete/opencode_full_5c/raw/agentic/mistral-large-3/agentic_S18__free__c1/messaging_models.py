from typing import Dict, Any, Optional
import json


class MessageRequest:
    """
    A class to represent a message request for Pub/Sub operations.
    """

    def __init__(
        self, data: Dict[str, Any], attributes: Optional[Dict[str, str]] = None
    ):
        self.data = data
        self.attributes = attributes or {}

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the message request to a dictionary.

        Returns:
            Dict[str, Any]: The message request as a dictionary.
        """
        return {"data": self.data, "attributes": self.attributes}


class MessageResponse:
    """
    A class to represent a message response from Pub/Sub operations.
    """

    def __init__(
        self,
        message_id: str,
        data: Dict[str, Any],
        attributes: Optional[Dict[str, str]] = None,
    ):
        self.message_id = message_id
        self.data = data
        self.attributes = attributes or {}

    @classmethod
    def from_dict(cls, response: Dict[str, Any]) -> "MessageResponse":
        """
        Creates a MessageResponse from a dictionary.

        Args:
            response: Dictionary containing response data.

        Returns:
            MessageResponse: The constructed MessageResponse.
        """
        return cls(
            message_id=response.get("message_id"),
            data=response.get("data", {}),
            attributes=response.get("attributes", {}),
        )


def normalize_message_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes message data to ensure consistent formatting.

    Args:
        data: The message data to normalize.

    Returns:
        Dict[str, Any]: The normalized message data.
    """
    normalized = {}
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            normalized[key] = json.loads(json.dumps(value))
        else:
            normalized[key] = value
    return normalized
