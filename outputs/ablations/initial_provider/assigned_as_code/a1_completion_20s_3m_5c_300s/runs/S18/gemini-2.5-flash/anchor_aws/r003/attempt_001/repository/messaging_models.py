import json

class Message:
    def __init__(self, message_id: str, payload: dict, attributes: dict = None):
        self.message_id = message_id
        self.payload = payload
        self.attributes = attributes if attributes is not None else {}

    def to_json(self):
        return json.dumps({
            "message_id": self.message_id,
            "payload": self.payload,
            "attributes": self.attributes
        })

    @classmethod
    def from_sqs_message(cls, sqs_message):
        body = json.loads(sqs_message['Body'])
        # Assuming SNS message structure within SQS
        if 'Message' in body and 'MessageId' in body:
            message_id = body['MessageId']
            payload = json.loads(body['Message'])
            attributes = body.get('MessageAttributes', {})
            return cls(message_id, payload, attributes)
        # Direct SQS message
        else:
            message_id = sqs_message['MessageId']
            payload = json.loads(sqs_message['Body'])
            attributes = sqs_message.get('MessageAttributes', {})
            return cls(message_id, payload, attributes)

class PublishRequest:
    def __init__(self, event: dict, attributes: dict = None):
        self.event = event
        self.attributes = attributes if attributes is not None else {}

class PublishResponse:
    def __init__(self, message_id: str):
        self.message_id = message_id

class ConsumeResponse:
    def __init__(self, message: Message, receipt_handle: str):
        self.message = message
        self.receipt_handle = receipt_handle
