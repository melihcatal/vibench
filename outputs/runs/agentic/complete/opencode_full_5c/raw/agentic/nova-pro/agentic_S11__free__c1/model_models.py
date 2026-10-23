class ModelRequest:
    def __init__(self, model_id, payload):
        self.model_id = model_id
        self.payload = payload


class ModelResponse:
    def __init__(self, response):
        self.response = response
