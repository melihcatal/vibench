class Message:
    def __init__(self, message_id, message_body):
        self.message_id = message_id
        self.message_body = message_body

    @staticmethod
    def from_sns_message(sns_message):
        return Message(
            message_id=sns_message['MessageId'],
            message_body=sns_message['Message']
        )

    @staticmethod
    def from_sqs_message(sqs_message):
        return Message(
            message_id=sqs_message['MessageId'],
            message_body=sqs_message['Body']
        )