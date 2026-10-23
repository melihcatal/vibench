class ModelRequest:
    def __init__(self, input_text):
        self.input_text = input_text


class ModelResponse:
    def __init__(self, text, usage, resource_id, model_handle):
        self.text = text
        self.usage = usage
        self.resource_id = resource_id
        self.model_handle = model_handle
