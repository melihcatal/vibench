class ModelRequest:
    def __init__(self, prompt, model='gpt-35-turbo'):
        self.prompt = prompt
        self.model = model

class ModelResponse:
    def __init__(self, content):
        self.content = content

def normalize_response(response):
    return ModelResponse(response['choices'][0]['message']['content'])