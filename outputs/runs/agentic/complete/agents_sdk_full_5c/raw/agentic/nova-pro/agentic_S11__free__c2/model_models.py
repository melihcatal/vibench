class ModelRequest:
    def __init__(self, model_id, input_text):
        self.model_id = model_id
        self.input_text = input_text

class ModelResponse:
    def __init__(self, text, sentiment):
        self.text = text
        self.sentiment = sentiment

def normalize_response(response):
    return ModelResponse(response.text, response.sentiment)