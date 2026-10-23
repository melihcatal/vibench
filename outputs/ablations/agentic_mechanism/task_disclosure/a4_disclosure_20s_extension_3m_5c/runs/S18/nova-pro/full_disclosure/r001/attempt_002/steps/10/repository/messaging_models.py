from typing import Any, Dict, List

class PubSubRequest:
    def __init__(self, topic: str, message: Dict[str, Any]):
        self.topic = topic
        self.message = message

    def to_dict(self) -> Dict[str, Any]:
        return {
            'topic': self.topic,
            'message': self.message
        }

class PubSubResponse:
    def __init__(self, status: str, message_id: str):
        self.status = status
        self.message_id = message_id

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PubSubResponse':
        return cls(
            status=data['status'],
            message_id=data['message_id']
        )

class PubSubNormalizer:
    @staticmethod
    def normalize_message(message: Dict[str, Any]) -> Dict[str, Any]:
        normalized_message = {
            'attributes': message.get('attributes', {}),
            'data': message.get('data', '')
        }
        return normalized_message

    @staticmethod
    def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
        normalized_response = {
            'status': response.get('status', ''),
            'message_id': response.get('message_id', '')
        }
        return normalized_response