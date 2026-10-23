class ModelRequest:
    def __init__(self, model, messages):
        self.model = model
        self.messages = messages

class ModelResponse:
    def __init__(self, content):
        self.content = content