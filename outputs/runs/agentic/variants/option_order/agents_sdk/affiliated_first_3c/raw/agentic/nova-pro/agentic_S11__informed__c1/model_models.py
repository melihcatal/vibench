class ModelRequest:
    def __init__(self, model_id, prompt):
        self.model_id = model_id
        self.prompt = prompt

class ModelResponse:
    def __init__(self, output, metadata):
        self.output = output
        self.metadata = metadata