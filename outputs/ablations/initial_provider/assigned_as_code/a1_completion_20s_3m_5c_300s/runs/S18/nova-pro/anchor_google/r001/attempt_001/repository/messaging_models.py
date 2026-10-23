class Message:
    def __init__(self, message_id, payload):
        self.message_id = message_id
        self.payload = payload

    @staticmethod
    def from_sns(sns_message):
        return Message(sns_message['MessageId'], json.loads(sns_message['Message']))

    @staticmethod
    def from_sqs(sqs_message):
        return Message(sqs_message['MessageId'], json.loads(sqs_message['Body']))