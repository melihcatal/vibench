from botocore.exceptions import ClientError


class PubSubMessage:
    def __init__(self, message_body):
        self.message_body = message_body

    @staticmethod
    def normalize(message):
        if isinstance(message, PubSubMessage):
            return message.message_body
        return message


class PubSubResponse:
    def __init__(self, response):
        self.response = response

    @staticmethod
    def parse(response):
        if isinstance(response, PubSubResponse):
            return response.response
        return response
