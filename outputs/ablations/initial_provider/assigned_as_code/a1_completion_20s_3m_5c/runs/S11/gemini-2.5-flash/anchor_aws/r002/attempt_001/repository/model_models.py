class ModelRequest:
    def __init__(self, text: str, model_id: str = "us.amazon.nova-pro-v1:0"):
        self.text = text
        self.model_id = model_id

class ModelResponse:
    def __init__(self, text: str, usage: dict = None, stop_reason: str = None):
        self.text = text
        self.usage = usage
        self.stop_reason = stop_reason
