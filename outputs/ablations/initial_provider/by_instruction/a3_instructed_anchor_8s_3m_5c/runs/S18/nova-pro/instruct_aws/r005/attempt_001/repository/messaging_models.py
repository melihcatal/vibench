class Message:
    def __init__(self, body):
        self.body = body

    @staticmethod
    def from_sns(sns_message):
        return Message(sns_message['Message'])

    @staticmethod
    def from_sqs(sqs_message):
        return Message(sqs_message['Body'])