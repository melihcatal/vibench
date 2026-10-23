class ModelRequest:
    def __init__(self, model, messages, temperature, max_tokens):
        self.model = model
        self.messages = messages
        self.temperature = temperature
        self.max_tokens = max_tokens

class ModelResponse:
    def __init__(self, content):
        self.content = content