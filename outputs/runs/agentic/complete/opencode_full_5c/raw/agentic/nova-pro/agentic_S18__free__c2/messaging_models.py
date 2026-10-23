class Message:
    def __init__(self, body, attributes=None):
        self.body = body
        self.attributes = attributes or {}

    @staticmethod
    def from_sns_message(sns_message):
        return Message(
            body=sns_message["Message"],
            attributes=sns_message.get("MessageAttributes", {}),
        )
