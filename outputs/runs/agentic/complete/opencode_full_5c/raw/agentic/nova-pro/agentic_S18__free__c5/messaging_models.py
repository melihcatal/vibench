class Message:
    def __init__(self, body, attributes):
        self.body = body
        self.attributes = attributes

    @staticmethod
    def normalize(raw_message):
        return Message(
            body=raw_message["Body"],
            attributes=raw_message.get("MessageAttributes", {}),
        )
