class ModelRequest:
    def __init__(self, model_id, prompt, max_tokens=50):
        self.model_id = model_id
        self.prompt = prompt
        self.max_tokens = max_tokens


class ModelResponse:
    def __init__(self, output_text, metadata):
        self.output_text = output_text
        self.metadata = metadata
