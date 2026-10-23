class ModelRequest:
    def __init__(self, text):
        self.text = text

class ModelResponse:
    def __init__(self, summary):
        self.summary = summary

def normalize_response(response):
    return ModelResponse(response.summary)