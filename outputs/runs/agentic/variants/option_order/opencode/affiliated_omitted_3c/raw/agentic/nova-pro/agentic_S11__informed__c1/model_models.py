class ModelRequest:
    def __init__(self, prompt, max_tokens):
        self.prompt = prompt
        self.max_tokens = max_tokens


class ModelResponse:
    def __init__(self, text, usage, model):
        self.text = text
        self.usage = usage
        self.model = model
