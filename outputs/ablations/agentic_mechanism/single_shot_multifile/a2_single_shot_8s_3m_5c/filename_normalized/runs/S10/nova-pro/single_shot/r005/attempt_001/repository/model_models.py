class ModelRequest:
    def __init__(self, model, params):
        self.model = model
        self.params = params

class ModelResponse:
    def __init__(self, response):
        self.response = response

    def normalize(self):
        return self.response['choices'][0]['text'].strip()
