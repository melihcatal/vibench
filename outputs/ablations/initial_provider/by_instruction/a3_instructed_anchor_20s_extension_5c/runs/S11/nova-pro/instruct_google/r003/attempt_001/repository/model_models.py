class ModelRequest:
    def __init__(self, instances):
        self.instances = instances

class ModelResponse:
    def __init__(self, predictions, metadata):
        self.predictions = predictions
        self.metadata = metadata
