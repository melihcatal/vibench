class ModelRequest:
    def __init__(self, prompt, max_tokens):
        self.prompt = prompt
        self.max_tokens = max_tokens


class ModelResponse:
    def __init__(self, text):
        self.text = text


def normalize_response(response):
    return ModelResponse(response["completion"])
