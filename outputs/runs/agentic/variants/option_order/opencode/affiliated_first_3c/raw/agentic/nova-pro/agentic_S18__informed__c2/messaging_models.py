class Message:
    def __init__(self, body):
        self.body = body


class Response:
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body
