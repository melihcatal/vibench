class Request:
    def __init__(self, model, messages):
        self.model = model
        self.messages = messages

class Response:
    def __init__(self, content):
        self.content = content