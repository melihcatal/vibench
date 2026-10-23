class ModelRequest:
    def __init__(self, text, model_id):
        self.text = text
        self.model_id = model_id


class ModelResponse:
    def __init__(self, text):
        self.text = text
