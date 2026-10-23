class NormalizePayload:
    def __init__(self, payload):
        self.payload = payload

    def __str__(self):
        return self.payload


class NormalizeResponse:
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return str(self.response)