class ModelRequest:
    def __init__(self, prompt, model="claude-3-opus-20240229"):
        self.prompt = prompt
        self.model = model


class ModelResponse:
    def __init__(self, content):
        self.content = content


def normalize_response(response):
    return ModelResponse(response.content)
