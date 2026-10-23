class ModelRequest:
    def __init__(self, text: str):
        self.text = text

    def to_dict(self):
        return {"text": self.text}

class ModelResponse:
    def __init__(self, text: str, metadata: dict = None):
        self.text = text
        self.metadata = metadata if metadata is not None else {}

    def to_dict(self):
        return {"text": self.text, "metadata": self.metadata}
