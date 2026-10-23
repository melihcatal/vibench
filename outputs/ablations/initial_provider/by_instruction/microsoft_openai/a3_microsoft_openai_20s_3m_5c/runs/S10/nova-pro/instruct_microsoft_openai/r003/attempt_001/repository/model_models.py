class ModelRequest:
    def __init__(self, model, prompt, max_tokens):
        self.model = model
        self.prompt = prompt
        self.max_tokens = max_tokens

class ModelResponse:
    def __init__(self, text):
        self.text = text

def normalize_response(response):
    return ModelResponse(response.choices[0].text.strip())