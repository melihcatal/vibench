import os
import json
from typing import Optional, Dict, Any
from azure.servicebus import ServiceBusClient


class MessagingClient:
    """Local configuration and client helper utilities for Azure Service Bus."""

    def __init__(self, connection_string: Optional[str] = None):
        self.connection_string = connection_string or os.getenv(
            "AZURE_SERVICE_BUS_CONNECTION_STRING"
        )
        if not self.connection_string:
            raise ValueError("Azure Service Bus connection string not provided")

        self._client = None

    @property
    def client(self) -> ServiceBusClient:
        """Lazy-loaded ServiceBusClient instance."""
        if self._client is None:
            self._client = ServiceBusClient.from_connection_string(
                self.connection_string
            )
        return self._client

    def close(self):
        """Close the client connection."""
        if self._client:
            self._client.close()
            self._client = None

    def get_topic_sender(self, topic_name: str):
        """Get a topic sender with context manager support."""
        return self.client.get_topic_sender(topic_name)

    def get_subscription_receiver(
        self, topic_name: str, subscription_name: str, max_wait_time: int = 5
    ):
        """Get a subscription receiver with context manager support."""
        return self.client.get_subscription_receiver(
            topic_name=topic_name,
            subscription_name=subscription_name,
            max_wait_time=max_wait_time,
        )

    @staticmethod
    def normalize_payload(payload: Any) -> Dict[str, Any]:
        """Normalize message payload to dictionary format."""
        if isinstance(payload, dict):
            return payload
        elif isinstance(payload, str):
            try:
                return json.loads(payload)
            except json.JSONDecodeError:
                return {"raw_data": payload}
        else:
            return {"data": str(payload)}

    @staticmethod
    def create_message_body(payload: Any, metadata: Optional[Dict] = None) -> bytes:
        """Create message body with optional metadata."""
        normalized = MessagingClient.normalize_payload(payload)
        if metadata:
            normalized["_metadata"] = metadata
        return json.dumps(normalized).encode("utf-8")

    @staticmethod
    def parse_message_body(body: bytes) -> Dict[str, Any]:
        """Parse message body from bytes to dictionary."""
        try:
            return json.loads(body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise ValueError(f"Failed to parse message body: {e}")
