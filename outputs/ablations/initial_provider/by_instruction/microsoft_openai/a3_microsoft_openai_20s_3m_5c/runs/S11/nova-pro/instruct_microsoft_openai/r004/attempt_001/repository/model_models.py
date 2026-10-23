class ModelRequest:
    def __init__(self, model_id, prompt, max_tokens=150):
        self.model_id = model_id
        self.prompt = prompt
        self.max_tokens = max_tokens

class ModelResponse:
    def __init__(self, output, usage):
        self.output = output
        self.usage = usage