class Request:
    def __init__(self, task, model, inputs):
        self.task = task
        self.model = model
        self.inputs = inputs

class Response:
    def __init__(self, outputs):
        self.outputs = outputs