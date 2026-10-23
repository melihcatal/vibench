class Payload:
    def __init__(self, object_name, data, content_type="application/octet-stream"):
        self.object_name = object_name
        self.data = data
        self.content_type = content_type


class Response:
    def __init__(self, status, message):
        self.status = status
        self.message = message