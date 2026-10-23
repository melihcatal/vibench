import json
from typing import Any, Dict, List, Optional

class Message:
    def __init__(self, message_id: str, body: str, attributes: Optional[Dict[str, str]] = None):
        self.message_id = message_id
        self.body = body
        self.attributes = attributes if attributes is not None else {}

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "body": self.body,
            "attributes": self.attributes
        }

    @classmethod
    def from_sqs_message(cls, sqs_message: Dict[str, Any]):
        message_id = sqs_message.get("MessageId") or sqs_message.get("MessageId") # For SQS, MessageId can be in different places
        body = sqs_message.get("Body", "{}")
        attributes = sqs_message.get("MessageAttributes", {})
        # Normalize SQS MessageAttributes to a simpler dict
        normalized_attributes = {
            k: v.get("StringValue") for k, v in attributes.items() if v.get("StringValue")
        }
        return cls(message_id=message_id, body=body, attributes=normalized_attributes)

class PublishResponse:
    def __init__(self, message_id: str, sequence_number: Optional[str] = None):
        self.message_id = message_id
        self.sequence_number = sequence_number

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "sequence_number": self.sequence_number
        }

class BatchPublishRequest:
    def __init__(self, messages: List[Dict[str, Any]]):
        self.messages = messages

    def to_sns_entries(self):
        entries = []
        for i, msg in enumerate(self.messages):
            entries.append({
                'Id': msg.get('Id', str(i)),
                'Message': json.dumps(msg.get('Message')),
                'Subject': msg.get('Subject', 'Batch Message'),
                'MessageAttributes': {
                    k: {'DataType': 'String', 'StringValue': str(v)} 
                    for k, v in msg.get('MessageAttributes', {}).items()
                }
            })
        return entries

class BatchPublishResponse:
    def __init__(self, successful: List[Dict[str, str]], failed: List[Dict[str, Any]]):
        self.successful = successful
        self.failed = failed

    def to_dict(self):
        return {
            "successful": self.successful,
            "failed": self.failed
        }

