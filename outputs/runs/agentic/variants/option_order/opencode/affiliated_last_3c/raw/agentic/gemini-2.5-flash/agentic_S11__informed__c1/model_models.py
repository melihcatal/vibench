class ModelRequest:
    def __init__(self, prompt: str, temperature: float = 0.7):
        self.prompt = prompt
        self.temperature = temperature


class ModelResponse:
    def __init__(self, text: str, finish_reason: str = None, token_usage: int = None):
        self.text = text
        self.finish_reason = finish_reason
        self.token_usage = token_usage
