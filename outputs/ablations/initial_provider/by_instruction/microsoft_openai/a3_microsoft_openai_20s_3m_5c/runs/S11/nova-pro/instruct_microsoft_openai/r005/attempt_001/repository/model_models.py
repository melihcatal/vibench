class ModelRequest:
    def __init__(self, model_id, messages):
        self.model_id = model_id
        self.messages = messages

class ModelResponse:
    def __init__(self, response):
        self.response = response

    def normalize(self):
        return {
            'content': self.response.choices[0].message.content,
            'usage': self.response.usage
        }