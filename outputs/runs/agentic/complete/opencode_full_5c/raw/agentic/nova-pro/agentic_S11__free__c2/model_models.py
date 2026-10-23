class ModelRequest:
    def __init__(self, model_id, input_data):
        self.model_id = model_id
        self.input_data = input_data


class ModelResponse:
    def __init__(self, output, metadata):
        self.output = output
        self.metadata = metadata
