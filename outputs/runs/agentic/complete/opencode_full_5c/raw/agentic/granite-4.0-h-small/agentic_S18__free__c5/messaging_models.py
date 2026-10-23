# messaging_models.py
"""
Local helper file: messaging_models.py
Defines request/response data models and helper normalization utilities for Pub/Sub Messaging.
"""


class PubSubEvent:
    """Represents an event that will be published to Pub/Sub.

    Attributes:
        payload (dict): The JSON-serializable payload to send.
        attributes (dict, optional): Optional metadata to include with the message.
    """

    def __init__(self, payload: dict, attributes: dict | None = None):
        self.payload = payload
        self.attributes = attributes or {}


class PubSubResult:
    """Wrapper for results returned from Pub/Sub operations.

    Attributes:
        message_id (str | None): The message ID returned by the provider, if any.
        error (str | None): Error message if processing failed.
    """

    def __init__(self, message_id: str | None = None, error: str | None = None):
        self.message_id = message_id
        self.error = error
