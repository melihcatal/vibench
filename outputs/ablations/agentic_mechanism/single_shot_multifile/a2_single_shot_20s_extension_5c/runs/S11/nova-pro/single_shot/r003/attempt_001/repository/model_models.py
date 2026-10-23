class ModelRequest:
    def __init__(self, prompt, max_tokens):
        self.prompt = prompt
        self.max_tokens = max_tokens

class ModelResponse:
    def __init__(self, text, usage):
        self.text = text
        self.usage = usage

def normalize_response(response):
    return ModelResponse(response.choices[0].text.strip(), response.usage)