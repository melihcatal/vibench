class ModelRequest:
    def __init__(self, model_id, input_text):
        self.model_id = model_id
        self.input_text = input_text

class ModelResponse:
    def __init__(self, body):
        self.body = body