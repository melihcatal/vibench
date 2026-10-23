
from typing import Dict, Any

class PubSubMessage:
    def __init__(self, data: bytes, attributes: Dict[str, str]):
        self.data = data
        self.attributes = attributes

class PubSubRequest:
    def __init__(self, topic: str, message: PubSubMessage):
        self.topic = topic
        self.message = message

class PubSubResponse:
    def __init__(self, message_id: str):
        self.message_id = message_id

class MessageNormalizer:
    @staticmethod
    def normalize_request(raw_data: Dict[str, Any]) -> PubSubRequest:
        # Placeholder for normalization logic
        # This would typically involve validating raw_data and converting it
        # into a PubSubRequest object.
        topic = raw_data.get("topic", "default-topic")
        data = raw_data.get("data", "").encode("utf-8")
        attributes = raw_data.get("attributes", {})
        message = PubSubMessage(data=data, attributes=attributes)
        return PubSubRequest(topic=topic, message=message)

    @staticmethod
    def normalize_response(raw_response: Dict[str, Any]) -> PubSubResponse:
        # Placeholder for normalization logic
        # This would typically involve extracting the message_id from the
        # raw response from the Pub/Sub API.
        message_id = raw_response.get("messageId", "unknown")
        return PubSubResponse(message_id=message_id)
