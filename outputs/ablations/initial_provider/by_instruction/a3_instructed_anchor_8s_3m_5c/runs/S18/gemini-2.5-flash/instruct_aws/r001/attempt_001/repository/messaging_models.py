import json
from typing import Dict, Any

class PubsubMessage:
    def __init__(self, message_id: str, data: Dict[str, Any], attributes: Dict[str, str]):
        self.message_id = message_id
        self.data = data
        self.attributes = attributes

    def to_json_string(self) -> str:
        return json.dumps(self.data)

    @classmethod
    def from_aws_sns(cls, sns_message: Dict[str, Any]):
        message_id = sns_message.get("MessageId", "N/A")
        message_body = json.loads(sns_message.get("Message", "{}"))
        attributes = sns_message.get("MessageAttributes", {})
        # AWS SNS MessageAttributes are more complex, we'll simplify for this model
        simple_attributes = {k: v["Value"] for k, v in attributes.items()}
        return cls(message_id, message_body, simple_attributes)
