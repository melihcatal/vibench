class ModelRequest:
    def __init__(self, prompt, model_id):
        self.prompt = prompt
        self.model_id = model_id


class ModelResponse:
    def __init__(self, output_text):
        self.output_text = output_text
